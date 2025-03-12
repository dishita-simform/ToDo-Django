from django.urls import path
from django.contrib.auth.views import LogoutView
from todo_app import admin
from . import views
from .views import user_login, user_logout

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task_list'),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('task/new/', views.task_create, name='task_create'),  # Create task
    path('tasks/add/', views.task_create, name='task_create'),
    path('task/edit/<int:pk>/', views.task_update, name='task_update'),  # Edit task
    path('task/delete/<int:pk>/', views.task_delete, name='task_delete'),
]