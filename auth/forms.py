from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterationForm(forms.Form):
    username = forms.CharField(label='UserName', required=True)
    first_name = forms.CharField(label='First Name', required=True, max_length=50)
    last_name = forms.CharField(label='Last Name', required=True, max_length=50)
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput())
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username already exists')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise ValidationError('Your password must be longer than 6 characters')
        return password

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

    def save(self, commit=True):
        user = super(RegisterationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='UserName', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise ValidationError('This user not exists')
        return username