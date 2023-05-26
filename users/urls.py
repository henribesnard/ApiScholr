from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('api/users/', views.UserCreateViewSet.as_view({'post': 'create'}), name='user-create'),
    path('api/set-password/', views.SetPasswordView.as_view(), name='set-password'),
    path('api/users_by_headstaff/', views.UserCreateByHeadStaffView.as_view(), name='user-create-by-headstaff'),
    path('api/update_profile/<int:pk>/', views.UserUpdateView.as_view(), name='update-profile'),

]
