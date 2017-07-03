from django import forms
from .models import Genre, File


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['file_name', 'file']


class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = ['genre_name', 'about_genre', 'genre_image']
