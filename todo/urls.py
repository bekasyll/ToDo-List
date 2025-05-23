from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name="todo_list"),
    path('signup/', views.signup_user, name="signup"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('edit/<int:pk>', views.edit_task, name="edit"),
    path('delete/<int:pk>', views.delete_task, name="delete"),
]
