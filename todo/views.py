from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import ToDo

from todo.forms import RegisterUserForm, LoginUserForm, ToDoForm


def index(request: HttpRequest):
    return redirect("signup")

def signup_user(request: HttpRequest):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            return redirect("login")
    else:
        form = RegisterUserForm()
    return render(request, "todo/signup.html", {"title": "Sign up", "form": form})

def login_user(request: HttpRequest):
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])

            if user and user.is_active:
                login(request, user)
                return redirect("todo_list")
            else:
                return redirect("login")
    else:
        form = LoginUserForm()
    return render(request, "todo/login.html", {"title": "Log in", "form": form})

@login_required
def todo_list(request: HttpRequest):
    if request.method == "POST":
        form = ToDoForm(request.POST)
        if form.is_valid():
            try:
                todo = form.save(commit=False)
                todo.user = request.user
                todo.save()
                return redirect("todo_list")
            except:
                form.add_error(None, "Error adding task!")
    else:
        form = ToDoForm()

    res = ToDo.objects.filter(user=request.user)
    return render(request, "todo/todo_list.html", {"title": "Get Things Done", "form": form, "res": res})

@login_required
def logout_user(request: HttpRequest):
    logout(request)
    return redirect("login")

@login_required
def edit_task(request: HttpRequest, pk):
    task = get_object_or_404(ToDo, id=pk, user=request.user)

    if request.method == "POST":
        form = ToDoForm(request.POST, instance=task, action="edit")
        if form.is_valid():
            try:
                task.save()
                return redirect("todo_list")
            except:
                form.add_error(None, "Error updating task!")
    else:
        form = ToDoForm(instance=task, action="edit")

    return render(request, "todo/edit_task.html", {"title": "Get Things Done", "form": form, "res": task})

@login_required
def delete_task(request: HttpRequest, pk):
    task = get_object_or_404(ToDo, id=pk, user=request.user)

    if request.method == "GET":
        task.delete()
    return redirect("todo_list")

def page_not_found(request: HttpRequest, exception):
    return render(request, "todo/page_not_found.html")
