from django import forms
from .models import Reference
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ['title', 'content', 'file']
    file = forms.FileField(required=True)


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

class CustomSignUpForm(UserCreationForm):
    # 아이디에 대한 유효성 검사
    username = forms.CharField(
        label="아이디",
        min_length=4,
        max_length=30,
        help_text="4자 이상 30자 이하로 입력해주세요."
    )

    # 비밀번호에 대한 유효성 검사
    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput,
        min_length=8,
        max_length=128,
        help_text="8자 이상 입력해주세요."
    )

    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput,
        min_length=8,
        max_length=128,
        help_text="위에서 입력한 비밀번호를 다시 입력해주세요."
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
