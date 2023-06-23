from .serializers import (CustomTokenObtainPairSerializer, UserSerializer, UserCreateSerializer, UserCreateByHeadStaffSerializer,
                           UserUpdateSerializer, RoleSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework import viewsets
from ApiScholr.permissions import IsAdminUser, IsHeadOrStaffUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, status, views
from rest_framework.response import Response
from .models import Role


User = get_user_model()


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if self.request.user.is_staff:
            user_id = self.request.GET.get('id', None)
            if user_id is not None:
                try:
                    return User.objects.get(id=user_id)
                except User.DoesNotExist:
                    raise Http404(_('User does not exist'))
        return self.request.user

class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdminUser]


class SetPasswordView(views.APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not user.check_password(current_password):
            return Response({"current_password": [_("Current password is not correct.")]}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        if new_password is None or new_password == '':
            return Response({"new_password": [_("New password must not be empty.")]}, 
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserCreateByHeadStaffView(CreateAPIView):
    serializer_class = UserCreateByHeadStaffSerializer
    permission_classes = [IsHeadOrStaffUser]

class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_roles = [role.name for role in user.roles.all()]

        if user.is_staff:
            return User.objects.all()
        elif set(user_roles).intersection(['HEAD', 'STAFF']):
            return User.objects.filter(establishments=user.current_establishment)
        else:
            return User.objects.filter(id=user.id)
