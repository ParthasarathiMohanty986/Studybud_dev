from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User
from django import forms


class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__'
        exclude=['participants','host']

# User Form for Editing Profile
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


#khali rakh diya hun login form.. Lekin use nahi haua hai kahi v
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. dennis_ivy',  # Optional placeholder
            'class': 'form__group',  # Use the same class as your user form for consistency
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',  # Optional placeholder
            'class': 'form__group',  # Same class for styling consistency
        })
    )
