from django import forms
from .models import BlogPost
from django.contrib.auth.forms import UserCreationForm
from .models import Comment


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'status', 'image']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)# add email field

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content',]