from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import RegisterForm, TaskForm

def home(request):
    image_url = "https://images.pexels.com/photos/4050315/pexels-photo-4050315.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    return render(request, "home.html", {"image_url": image_url})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')  # Ensure email is saved
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('task_list')  # Ensure this matches the correct URL name
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

### 🚀 **CRUD Operations - Now Require Login**

@login_required
def task_list(request):
    """ View all tasks for the logged-in user """
    tasks = Task.objects.filter(user=request.user)
    completed_tasks = tasks.filter(completed=True)
    pending_tasks = tasks.filter(completed=False)
    return render(request, 'task_list.html', {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks
    })

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the task to the logged-in user
            task.save()
            return redirect('task_list')  # Redirect to the task list
    else:
        form = TaskForm()
    
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    """ Update an existing task - Only for the task owner """
    task = get_object_or_404(Task, pk=pk, user=request.user)  # Ensures the user owns the task
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
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    
    return render(request, 'task_confirm_delete.html', {'task': task})  # This should only be called when deleting
