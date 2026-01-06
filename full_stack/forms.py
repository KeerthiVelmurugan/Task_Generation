from django import forms
from .models import Language, Concept

class TaskGeneratorForm(forms.Form):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    concepts = forms.ModelMultipleChoiceField(
        queryset=Concept.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    number_of_tasks = forms.IntegerField(min_value=1, label="Number of Tasks")


class TaskGeneratorForms(forms.Form):

    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'id': 'id_languages'
        })
    )

    concepts = forms.ModelMultipleChoiceField(
        queryset=Concept.objects.none(),   # IMPORTANT
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'id': 'id_concepts'
        })
    )

    number_of_tasks = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )
    
    
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

from django import forms
from .models import Language, Concept, Task

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name']


class ConceptForm(forms.ModelForm):
    class Meta:
        model = Concept
        fields = ['language', 'name']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['concept', 'description']
        
from django import forms
from .models import Intern

class InternForm(forms.ModelForm):
    class Meta:
        model = Intern
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone'}),
        }

