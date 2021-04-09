from rest_framework import mixins, status, viewsets
from django.http import HttpResponseRedirect
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated
)

from admincu.users.permissions import IsAccountOwner

from admincu.users.serializers import (
	UserModelSerializer,
	PerfilModelSerializer,
	UserSignupSerializer,
	UserLoginSerializer,
	AccountVerificationSerializer,
	PasswordRecoverySerializer,
	ChangePasswordSerializer,
)
from admincu.users.models import (
	User,
)

from admincu.utils.serializers import (
	ComunidadModelSerializer
)

class UserViewSet(mixins.RetrieveModelMixin, 
				  mixins.UpdateModelMixin,
				  viewsets.GenericViewSet):
	'''User View set'''
	

	queryset = User.objects.filter(is_active=True, is_verified=True)
	serializer_class = UserModelSerializer
	lookup_field = 'username'

	def get_permissions(self):
		'''Asigna permisos basandose en la accion'''
		if self.action in ['signup', 'verify', 'login', 'passwordRecovery', 'changePassword']:
			permissions = [AllowAny]
		elif self.action in ['retrive', 'update', 'partial_update']:
			permissions = [IsAuthenticated, IsAccountOwner]
		else:
			permissions = [IsAuthenticated]
		return [p() for p in permissions]


	@action(detail=False, methods=['post'])
	def signup(self, request, *args, **kwargs):
		'''User signup'''
		serializer = UserSignupSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		data = {'message': 'Verifica tu cuenta!! Ha sido enviado un email de verificacion a tu correo electronico.'}
		return Response(data, status=status.HTTP_201_CREATED)


	@action(detail=False, methods=['get'])
	def verify(self, request, *args, **kwargs):
		'''Verificaciond de la cuenta'''

		serializer = AccountVerificationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return HttpResponseRedirect("https://admin-cu.com/login/")
		#return Response(data, status=status.HTTP_200_OK)


	@action(detail=False, methods=['post'])
	def login(self, request, *args, **kwargs):
		'''User login'''

		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user, token = serializer.save()
		perfil = user.perfil_set.first()
		if perfil:
			comunidad = perfil.comunidad
		data = {
			'comunidad' : ComunidadModelSerializer(comunidad).data if perfil else None,
			'perfil' : PerfilModelSerializer(perfil).data, 
			'user': UserModelSerializer(user).data,
			'access_token': token,
		}
		return Response(data, status=status.HTTP_201_CREATED)


	@action(detail=False, methods=['post'])
	def passwordRecovery(self, request, *args, **kwargs):
		'''Recuperacion de contraseña'''

		serializer = PasswordRecoverySerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		users = serializer.save()
		data = UserModelSerializer(users, many=True).data
		return Response(data, status=status.HTTP_201_CREATED)


	@action(detail=False, methods=['post'])
	def changePassword(self, request, *args, **kwargs):
		'''Cambio de contraseña'''

		serializer = ChangePasswordSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		data = UserModelSerializer(user).data
		return Response(data, status=status.HTTP_201_CREATED)