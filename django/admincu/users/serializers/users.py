from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from datetime import timedelta
import jwt

from admincu.users.serializers import PerfilModelSerializer
from admincu.users.models import (
    Perfil,
    User,
)
from admincu.utils.models import (
    Comunidad
)


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
    email = serializers.EmailField()
    comunidad = serializers.ChoiceField(Comunidad.objects.all())
    numero_documento = serializers.CharField(min_length=6, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        '''Verifica coincidencia de password'''
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        password_validation.validate_password(passwd)

        '''Verifica el documento en documentos de la comunnidad'''
        perfil = Perfil.objects.filter(comunidad=data['comunidad'], numero_documento=data['numero_documento'])
        if not perfil:
            raise serializers.ValidationError("Datos invalidos ponete en contacto con tu administracion.")
        return data

    def create(self, data):
        '''Creacion del user'''
        # Poner esto que esta comentado una vez que en el frontend se quiera realizar
        # data.pop('numero_documento')
        # data.pop('comunidad')
        # data.pop('password_confirmation')
        # user = User.objects.create_user(**data, is_verified=False)
        # self.send_confirmation_email(user)

        num_doc = data.pop('numero_documento')
        comunidad = data.pop('comunidad')
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=True)
        perfil = Perfil.objects.get(numero_documento=num_doc, comunidad=comunidad)
        perfil.users.add(user)



        user.groups.add(Group.objects.get(name='socio'))
        return user

    def send_confirmation_email(self, user):
        '''Envia el email para confirmar la cuenta'''
        verification_token = self.gen_verification_token(user)
        subject = "Bienvenido {} a AdminCU!!! Verifica tu cuenta...".format(user.username)
        from_email = 'AdminCU <noreply@admin-cu.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {'token': verification_token, 'user': user},
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

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

    comunidad = serializers.ChoiceField(Comunidad.objects.all())
    email = serializers.EmailField()
        
    def validate(self, data):
        '''Verifica el email en emails de usuarios de la comunnidad'''
        users = []
        for p in Perfil.objects.filter(comunidad=data['comunidad']):
            users.extend(p.users.filter(email=data['email'], is_verified=True, is_active=True))
        if not users:
            raise serializers.ValidationError("Email invalido.")
        self.context['users'] = users
        return data

    def create(self, data):
        '''Creacion del Token y envio de email de recuperacion por User vinculado al email en la comunidad.'''
        for user in self.context['users']:
            self.send_confirmation_email(user)
        return self.context['users']

    def send_confirmation_email(self, user):
        '''Envia email con token de recuperacion'''
        recovery_token = self.gen_recovery_token(user)
        subject = "Solicitud de recuperacion de clave: Usuario {}".format(user.username)
        from_email = 'AdminCU <noreply@admin-cu.com>'
        content = render_to_string(
            'emails/users/password_recovery.html',
            {'token': recovery_token, 'user': user},
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

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