from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TaskForm(forms.ModelForm):
    completed_at = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        label="Completed On"
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'completed_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Task details...'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        completed = cleaned_data.get("completed")
        completed_at = cleaned_data.get("completed_at")

        # If task is marked as completed but no completion date is provided, raise an error
        if completed and not completed_at:
            raise forms.ValidationError("Please provide a completion date when marking the task as completed.")

        return cleaned_data