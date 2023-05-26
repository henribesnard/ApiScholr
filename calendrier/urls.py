from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet, basename='room')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/timeslots/create/', views.TimeslotCreateView.as_view(), name='create_timeslot'),
    path('api/timeslots/update/<int:pk>/', views.TimeslotUpdateView.as_view(), name='update_timeslot'),
    path('api/timeslots/delete/<int:pk>/', views.TimeslotDeleteView.as_view(), name='delete_timeslot'),
    path('api/timeslots/', views.TimeslotListView.as_view({'get': 'list'}), name='timeslot_list'),
    path('api/timeslots/<int:pk>/', views.TimeslotListView.as_view({'get': 'retrieve'}), name='timeslot_detail'),
]
