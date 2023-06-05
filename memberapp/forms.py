from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    used = forms.IntegerField(label='사용횟수', required=False)
    paid = forms.BooleanField(label='유료회원', required=False)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "used", "paid")