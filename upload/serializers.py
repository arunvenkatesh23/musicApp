from rest_framework import serializers
from .models import Genre, File


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        # fields = '__all__'
        fields = ['id', 'user', 'genre_name', 'about_genre', 'genre_image', 'is_favorite']


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        # fields = '__all__'
        fields = ['id', 'user', 'genre', 'file_name', 'file', 'is_favorite']
