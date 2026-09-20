
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import MediaItem, Comment, Like
from django.core.exceptions import ValidationError

class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ['title', 'media_type', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 10 * 1024 * 1024: # 10 MB limit
                raise ValidationError("File size should not exceed 10 MB.")
        return file

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 5:
            raise ValidationError('Comment must be at least 5 characters long.')
        return content

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['media_item', 'user']
        
    def clean(self):
        cleaned_data = super().clean()
        media_item = cleaned_data.get('media_item')
        user = cleaned_data.get('user')

        if Like.objects.filter(media_item=media_item, user=user).exists():
            raise ValidationError("You have already liked this media item.")

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["username", "password"]
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError("Invalid username or password.")

