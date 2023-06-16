from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.utils.translation import gettext_lazy as _

from .models import User, Lead

# 

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(max_length=100, required=True,
                            widget=forms.EmailInput
                            (attrs={'class':'username_input', 'placeholder':'email'}))
    first_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'class':'firstname_input', 'placeholder':'first name'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput
                                (attrs={'class':'lastname_input', 'placeholder':'last name'}))
    password1 = forms.CharField(max_length=30, required=True,
                                widget=forms.PasswordInput
                                (attrs={'class':'password_input', 'placeholder':'password'}))
    password2 = forms.CharField(max_length=30, required=True,
                                widget=forms.PasswordInput
                                (attrs={'class':'password_input', 'placeholder':'verify password'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ('email','first_name', 'last_name')

class UserForm(forms.ModelForm):
    email= forms.CharField(max_length=100,
                           widget= forms.EmailInput
                           (attrs={'class':'username_input', 'placeholder':'Email'}))
    password = forms.CharField(max_length=30,
                                widget=forms.PasswordInput
                                (attrs={'class':'password_input', 'placeholder':'Password'}))
    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')

class LeadForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    contact_num = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Contact #'}))
    notes = forms.Textarea()
    id = forms.ModelChoiceField(queryset=Lead.objects.all() ,widget=forms.HiddenInput(), required=False)


    class Meta:
        model = Lead
        fields = ('first_name', 'last_name', 'email', 'contact_num', 'notes', ) 
        #'touches', 'status', 'intent', 'last_contacted', 'date_created', 'notes')
                

    
