from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from todo_app.models import Todo


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password1':'','password2':""}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html',{'form':form})
 

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'auth/login.html',{'form':form}) 
    
@login_required
def dashboard_view(request):
    # Add new task
    if request.method == "POST":
        task_title = request.POST.get("task")
        if task_title:
            Todo.objects.create(user=request.user, title=task_title)
            return redirect("dashboard")

    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "dashboard.html", {"todos": todos})

    


def logout_view(request):
    logout(request)
    return redirect('login')