from django import forms
from .models import Folder, File


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['file_name', 'file', 'genre']


class FolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = ['folder_name', 'about_file', 'folder_image']
