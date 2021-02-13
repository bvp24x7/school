from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        
        fields = ['username', 'email', 'password1', 'password2',]

class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ['enrollment', 'standard']


class QuizForm(forms.ModelForm):
    
    class Meta:
        model = Quiz
        fields = '__all__'

class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = '__all__'

class OptionsForm(forms.ModelForm):
    
    class Meta:
        model = Options
        fields = '__all__'



