from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "index"),
    path('login/', views.LoginAPI.as_view(), name = 'login'),
    path('profile/', views.ProfileAPI.as_view(), name = 'profile'),
    path('all_employees/', views.all_employees, name = 'all_employees'),
    path('view_employee/<str:pk>/', views.view_employee, name = 'view_employee'),
    path('location/', views.LocationAPI.as_view(), name = 'location'),
    path('attendance/', views.AttendanceAPI.as_view(), name = 'attendance'),
    path('project/', views.ProjectAPI.as_view(), name = 'project'),
    path('task/', views.TaskAPI.as_view(), name = 'task'),
    path('notification/', views.NotificationAPI.as_view(), name = 'notification'),
]