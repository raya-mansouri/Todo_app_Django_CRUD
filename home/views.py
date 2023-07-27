from django.shortcuts import render, redirect
from .models import Todo
from django.contrib import messages
from .forms import TodoCreateForm, TodoUpdateForm


# Create your views here.

def home(request):
    all_todos = Todo.objects.filter(user=request.user)
    return render(request, 'home.html', {'todos': all_todos})


def detail(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    return render(request, 'detail.html', {'todo': todo})


def delete(request, todo_id):
    Todo.objects.get(id=todo_id).delete()
    messages.success(request, 'Deleted Successfully', 'success')
    return redirect('home')


def create(request):
    if request.method == 'POST':
        form = TodoCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Todo.objects.create(user=request.user, title=cd['title'], body=cd['body'], created=cd['created'])
            messages.success(request, 'Todo added successfully', 'success')
            return redirect('home')
    else:
        form = TodoCreateForm
    return render(request, 'create.html', {'form': form})


def update(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    if request.method == 'POST':
        form = TodoUpdateForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'todo updated successfully', 'success')
            return redirect('details', todo_id)
    else:
        form = TodoUpdateForm(instance=todo)
    return render(request, 'update.html', {'form': form})
