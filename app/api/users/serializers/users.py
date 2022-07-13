from django.contrib.auth import authenticate, password_validation
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from datetime import timedelta
import jwt

from apps.communications.models import Queue

from apps.users.models import (
	Perfil,
	User,
)
from apps.utils.models import (
	Comunidad
)

from api.users.serializers import PerfilModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
	'''User model serializer'''

	perfil = PerfilModelSerializer(read_only=True)
	group = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = (
			'username',
			'email',
			'perfil',
			'group'
		)

	def get_group(self, obj):
		return obj.groups.first().name


class UserSignupSerializer(serializers.Serializer):
	'''User signup serializer.'''

	username = serializers.CharField(
		min_length=4,
		max_length=30,
		validators=[UniqueValidator(queryset=User.objects.all())]
	)
	first_name = serializers.CharField(min_length=2, max_length=64)
	last_name = serializers.CharField(min_length=2, max_length=64)
	email = serializers.EmailField()
	numero_documento = serializers.CharField(min_length=6, max_length=64)
	password = serializers.CharField(min_length=8, max_length=64)
	password_confirmation = serializers.CharField(min_length=8, max_length=64)


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['comunidad'] = serializers.ChoiceField(Comunidad.objects.all())

	def validate(self, data):
		'''Verifica que la comunidad no tenga simple solutions '''
		comunidad = data['comunidad']
		# if comunidad.accountss_set.all():
		# 	raise serializers.ValidationError({"comunidad": "La administracion de tu comunidad utiliza una plataforma externa de comunicacion."})

		'''Verifica el documento en documentos de la comunidad'''
		perfil = Perfil.objects.filter(comunidad=data['comunidad'], numero_documento=data['numero_documento'])
		if not perfil:
			raise serializers.ValidationError({"numero_documento": "Datos invalidos. Ponete en contacto con tu administracion."})

		'''Verifica coincidencia de password'''
		passwd = data['password']
		passwd_conf = data['password_confirmation']
		if passwd != passwd_conf:
			raise serializers.ValidationError({"password" : "Las contraseñas no coinciden."})
		password_validation.validate_password(passwd)

		return data

	def create(self, data):
		'''Creacion del user'''
		data.pop('numero_documento')
		data.pop('comunidad')
		data.pop('password_confirmation')
		user = User.objects.create_user(**data, is_verified=False)
		self.send_email(user)
		user.groups.add(Group.objects.get(name='socio'))
		return user

	def send_email(self, user):
		'''Envia el email para confirmar la cuenta'''
		verification_token = self.gen_verification_token(user)
		subject = "Bienvenido/a {} a AdminSmart! Verifica tu cuenta...".format(user.username)
		html_string = render_to_string(
			'emails/users/account_verification.html',
			context={
				'token': verification_token,
				'user': user,
			},
		)
		comunidad = perfil.comunidad,
		addressee = perfil,
		Queue.objects.create(
			comunidad=perfil.comunidad,
			addressee=perfil,
			subject=subject,
			body=html_string,
			client="users.serializers.UserSignupSerializer"
		)

	def gen_verification_token(self, user):
		'''General el token mediante jwt para enviar en el email de confirmacion'''
		exp_date = timezone.now() + timedelta(days=3)
		payload = {
			'user': user.username,
			'doc': self.data['numero_documento'],
			'com': self.data['comunidad'].id,
			'exp': int(exp_date.timestamp()),
			'type': 'email_confirmation'
		}
		token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
		return token.decode()


class AccountVerificationSerializer(serializers.Serializer):
	'''Account Verification Serializer'''

	token = serializers.CharField()

	def validate_token(self, data):
		'''Verificacion de token'''
		try:
			payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
		except jwt.ExpiredSignatureError:
			raise serializers.ValidationError('El link de verificacion ha expirado')
		except jwt.PyJWTError:
			raise serializers.ValidationError('Token invalido')
		if payload['type'] != 'email_confirmation':
			raise serializers.ValidationError('Token invalido')
		self.context['payload'] = payload
		return data

	def save(self):
		'''Cambia el usuario a activo y vincula el perfil'''
		payload = self.context['payload']
		user = User.objects.get(username=payload['user'])
		user.is_verified = True
		user.save()
		perfil = Perfil.objects.get(numero_documento=payload['doc'], comunidad__id=payload['com'])
		perfil.users.add(user)


class UserLoginSerializer(serializers.Serializer):
	'''User login serializer'''

	username = serializers.CharField(min_length=4, max_length=64)
	password = serializers.CharField(min_length=8, max_length=64)

	def validate(self, data):
		'''check credentials'''
		user = authenticate(username=data['username'], password=data['password'])
		if not user:
			raise serializers.ValidationError('Credenciales invalidas.')
		if not user.is_verified:
			raise serializers.ValidationError("La cuenta no se encuentra activa")
		self.context['user'] = user
		return data

	def create(self, data):
		'''Generate or retrive a new token'''
		token, created = Token.objects.get_or_create(user=self.context['user'])
		return self.context['user'], token.key


class PasswordRecoverySerializer(serializers.Serializer):
	'''Password recovery serializer'''

	email = serializers.EmailField()

	def validate(self, data):
		'''Verifica el email en emails de usuarios de la comunnidad'''
		users = []
		for p in Perfil.objects.all():
			users.extend(p.users.filter(email=data['email'], is_verified=True, is_active=True))
		if not users:
			raise serializers.ValidationError("Email invalido.")
		self.context['users'] = users
		return data

	def create(self, data):
		'''Creacion del Token y envio de email de recuperacion por User vinculado al email en la comunidad.'''
		for user in self.context['users']:
			self.send_email(user)
		return self.context['users']

	def send_email(self, user):
		'''Envia email con token de recuperacion'''
		recovery_token = self.gen_recovery_token(user)
		subject = "Solicitud de recuperacion de clave: Usuario {}".format(user.username)
		html_string = render_to_string(
			'emails/users/password_recovery.html',
			{'token': recovery_token, 'user': user},
		)
		perfil = user.perfil_set.first()
		Queue.objects.create(
			comunidad=perfil.comunidad,
			addressee=perfil,
			subject=subject,
			body=html_string,
			client="users.serializers.PasswordRecoverySerializer"
		)

	def gen_recovery_token(self, user):
		'''Generacion de token de recuperacion de password mediante jwt'''
		exp_date = timezone.now() + timedelta(days=1)
		payload = {
			'user': user.username,
			'exp': int(exp_date.timestamp()),
			'type': 'password_recovery'
		}
		token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
		return token.decode()


class ChangePasswordSerializer(serializers.Serializer):
	'''Change password Serializer'''

	token = serializers.CharField()
	password = serializers.CharField(min_length=8, max_length=64)
	password_confirmation = serializers.CharField(min_length=8, max_length=64)

	def validate(self, data):
		'''Verifica coincidencia de password'''
		passwd = data['password']
		passwd_conf = data['password_confirmation']
		if passwd != passwd_conf:
			raise serializers.ValidationError("Las contraseñas no coinciden.")
		password_validation.validate_password(passwd)
		return data

	def validate_token(self, data):
		'''Verificacion de token'''
		try:
			payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
		except jwt.ExpiredSignatureError:
			raise serializers.ValidationError('El link de verificacion ha expirado')
		except jwt.PyJWTError:
			raise serializers.ValidationError('Token invalido')
		if payload['type'] != 'password_recovery':
			raise serializers.ValidationError('Token invalido')
		self.context['payload'] = payload
		return data

	def save(self):
		'''Modifica contraseña'''
		payload = self.context['payload']
		user = User.objects.get(username=payload['user'])
		user.set_password (self.data['password'])
		user.save()
		return user


class ChangeCommunitySerializer(serializers.Serializer):
	'''Change password Serializer'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['comunidad'] = serializers.ChoiceField(Comunidad.objects.all())

	def validate(self, data):
		'''Verifica coincidencia de password'''

		user = self.context['user']
		if not data['comunidad'] in user.perfil_set.first().comunidades.all():
			raise serializers.ValidationError({'comunidad': "No puede acceder a la comunidad solicitada"})
		return data

	def save(self):
		'''Modifica contraseña'''

		user = self.context['user']
		perfil = user.perfil_set.first()
		perfil.comunidad = self.data['comunidad']
		perfil.save()
		return user
