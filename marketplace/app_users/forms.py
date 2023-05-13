from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.forms.widgets import FileInput

from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.auth.models import User
from django.forms.widgets import FileInput
from app_merch.models import Image
from .models import Profile


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Полное имя",
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
    )
    phone_number = forms.CharField(
        max_length=50,
        required=True,
        label="Номер телефона",
        widget=forms.TextInput(attrs={"placeholder": "Eg. +79991234567 "}),
    )
    address = forms.CharField(
        max_length=255,
        required=True,
        label="Адрес",
        widget=forms.TextInput(attrs={"placeholder": "Введите адрес"}),
    )
    avatar = forms.FileField(widget=FileInput, required=False, label="Аватар")

    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Введите пароль",
                "minlength": 8,
            }
        ),
        help_text="Пароль должен содержать не менее 8 символов и быть сложным",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Подтвердите пароль",
                "minlength": 8,
            }
        ),
        help_text="Введите пароль еще раз для подтверждения",
    )
    username = forms.CharField(
        max_length=50,
        required=True,
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"placeholder": "Введите имя пользователя"}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "full_name",
            "phone_number",
            "address",
            "avatar",
        ]
        labels = {
            "username": "Имя пользователя",
            "email": "Email",
        }
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Eg. mail@mail.com"}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True, label="Имя пользователя")
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Пароль"
    )

    class Meta:
        model = User
        fields = ["username", "password"]
        labels = {
            "username": "Имя пользователя",
            "password": "Пароль",
        }


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True, label="Email")

    class Meta:
        model = User
        fields = ["email"]
        labels = {
            "email": "Email",
        }


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Новый пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, required=True, label="Подтверждение нового пароля"
    )

    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]
        labels = {
            "new_password1": "Новый пароль",
            "new_password2": "Подтверждение нового пароля",
        }


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "id": "mail",
                    "name": "mail",
                    "data-validate": "require",
                }
            ),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "full_name",
            "phone_number",
        )
        widgets = {
            "phone_number": forms.TextInput(
                attrs={"class": "form-input", "id": "phone", "name": "phone"}
            ),
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "id": "name",
                    "name": "name",
                    "data-validate": "require",
                }
            ),
        }


class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "id": "password",
                "name": "password",
                "placeholder": "Тут можно изменить пароль",
            }
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "id": "passwordReply",
                "name": "passwordReply",
                "placeholder": "Введите пароль повторно",
            }
        ),
    )


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = "__all__"
        widgets = {
            "file": forms.ClearableFileInput(
                attrs={
                    "class": "Profile-file form-input",
                    "id": "avatar",
                    "name": "avatar",
                    "data-validate": "onlyImgAvatar",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(AvatarUpdateForm, self).__init__(*args, **kwargs)
        self.fields["title"].required = False

    def clean_file(self):
        file = self.cleaned_data.get("file", False)
        if file:
            if file.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Размер файла не должен превышать 2 МБ")
            return file
        else:
            raise forms.ValidationError("Не удалось загрузить файл")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.file.title = f"Аватар {self.request.user.username}"
        if commit:
            instance.save()
        return instance
