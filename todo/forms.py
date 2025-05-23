from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from prompt_toolkit.validation import ValidationError
from .models import ToDo


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Username:",
            widget=forms.TextInput(attrs={"class": "inp", "placeholder": "Username"}), required=True)
    password1 = forms.CharField(label="Password:",
            widget=forms.PasswordInput(attrs={"class": "inp", "placeholder": "Password"}), required=True)
    password2 = forms.CharField(label="Password again:",
            widget=forms.PasswordInput(attrs={"class": "inp", "placeholder": "Password again"}), required=True)
    email = forms.EmailField(label="Email",
            widget=forms.TextInput(attrs={"class": "inp", "placeholder": "Email"}), required=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match!")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")
        return email

class LoginUserForm(forms.Form):
    username = forms.CharField(label="Username or E-mail",
            widget=forms.TextInput(attrs={"class": "inp", "placeholder": "Username or E-mail"}))
    password = forms.CharField(label="Password",
            widget=forms.PasswordInput(attrs={"class": "inp", "placeholder" : "Password"}))

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ["title"]
        labels = {"title": "keep on going. you can do it."}
        widgets = {"title" : forms.TextInput(attrs={"class": "inp", "required": "required"})}

    def __init__(self, *args, **kwargs):
        action = kwargs.pop("action", "add")
        super().__init__(*args, **kwargs)

        if action == "edit":
            placeholder = "Update your task"
        else:
            placeholder = "Add your task"

        self.fields["title"].widget.attrs.update({'placeholder':placeholder})

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 25:
            raise ValidationError("The length exceeds 25 characters!")
        return title


