from django.urls import path
from django.contrib.auth.views import LogoutView
from todo_app import admin
from . import views
from .views import user_login

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task-list'),
    path("login/", user_login, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path('register/', views.register, name='register'),
    path('', views.task_list, name='task_list'),  # View all tasks
    path('task/new/', views.task_create, name='task_create'),  # Create task
    path('tasks/add/', views.task_create, name='task_create'),
    path('task/edit/<int:pk>/', views.task_update, name='task_update'),  # Edit task
    path('task/delete/<int:pk>/', views.task_delete, name='task_delete'),
]