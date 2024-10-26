
from django import forms
from .models import FileRepositoryI

class FileRepositoryIForm(forms.ModelForm):
    class Meta:
        model = FileRepositoryI
        fields = ['college', 'department', 'author','degree_level', 'catagory', 'file_name']
