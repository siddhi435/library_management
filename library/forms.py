from django import forms
from .models import Book, Member, Issue
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address', 'password1', 'password2']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'quantity', 'status']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['book', 'member', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReturnForm(forms.Form):
    issue_id = forms.IntegerField(widget=forms.HiddenInput())