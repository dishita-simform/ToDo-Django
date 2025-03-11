from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task
from .forms import RegisterForm, TaskForm, CustomLoginForm

def home(request):
    image_url = "https://images.pexels.com/photos/4050315/pexels-photo-4050315.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    return render(request, "home.html", {"image_url": image_url})

def register(request):
    """ Handles user registration """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    """ Allows users to log in with either email or username """
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Check if input is an email
            user = User.objects.filter(email=username_or_email).first()
            if user:
                username = user.username  # Get the username from email
            else:
                username = username_or_email  # If not an email, assume it's a username

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('task_list')

    else:
        form = CustomLoginForm()
    
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

### 🚀 **Task CRUD Operations (Require Login)**

@login_required
def task_list(request):
    """ View all tasks for the logged-in user """
    tasks = Task.objects.filter(user=request.user)
    completed_tasks = tasks.filter(completed=True)
    pending_tasks = tasks.filter(completed=False)
    return render(request, 'task_list.html', {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'first_name': request.user.first_name  # Display first name
    })

@login_required
def task_create(request):
    """ Create a new task """
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the task to the logged-in user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    """ Update an existing task (only if the user owns it) """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    """ Delete a task (only if the user owns it) """
    task = get_object_or_404(Task, pk=pk, user=request.user)  # Ensure user owns the task
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    
    return render(request, 'task_confirm_delete.html', {'task': task})