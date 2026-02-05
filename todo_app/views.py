from django.shortcuts import render, redirect
from .models import Todo
from django.contrib.auth.decorators import login_required

@login_required
def todo_index(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')

    if request.method == "POST":
        task_title = request.POST.get("task")
        if task_title:
            Todo.objects.create(user=request.user, title=task_title)
            return redirect("todo_index")

    return render(request, "todo/index.html", {"todos": todos})

@login_required
def toggle_complete(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect("dashboard")

@login_required
def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.delete()
    return redirect("dashboard")


