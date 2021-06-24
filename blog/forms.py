from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Comment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio','first_name','last_name','country','qul','mob']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class SharedForm(forms.Form):
    title = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':'3', 'placeholder': 'Say something'}))

