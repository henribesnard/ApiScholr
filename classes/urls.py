from django.urls import path
from . import views

urlpatterns = [
    path('api/create_class/', views.CreateSchoolclassView.as_view(), name='create_class'),
    path('api/create_course/', views.CreateCourseView.as_view(), name='create_course'),
    path('api/update/schoolclasses/<int:pk>/', views.SchoolclassUpdateView.as_view(), name='update_class'),
    path('api/update/course/<int:pk>/', views.CourseUpdateView.as_view(), name='update_course'),
    path('api/classes/', views.SchoolclassListView.as_view(), name='class_list'),
    path('api/classes/<int:pk>/', views.SchoolclassDetailView.as_view(), name='class_detail'),
    path('api/courses/', views.CourseListView.as_view(), name='course_list'),
    path('api/courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),

]
