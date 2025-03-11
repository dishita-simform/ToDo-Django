from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task-list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.task_list, name='task_list'),  # View all tasks
    path('task/new/', views.task_create, name='task_create'),  # Create task
    path('tasks/add/', views.task_create, name='task_create'),
    path('task/edit/<int:pk>/', views.task_update, name='task_update'),  # Edit task
    path('task/delete/<int:pk>/', views.task_delete, name='task_delete'),
]