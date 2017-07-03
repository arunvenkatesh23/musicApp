from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db.models import Q
from .forms import FileForm, GenreForm
from .models import Genre, File
from rest_framework import viewsets
from .serializers import GenreSerializer, FileSerializer


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('-id')
    serializer_class = GenreSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('-id')
    serializer_class = FileSerializer


def create_folder(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        form = GenreForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            genre = form.save(commit=False)
            genre.user = request.user
            genre.genre_image = request.FILES['genre_image']
            file_type = genre.genre_image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'genre': genre,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'upload/folder_form.html', context)
            genre.save()
            return render(request, 'upload/detail.html', {'genre': genre})
        context = {
            "form": form,
        }
        return render(request, 'upload/folder_form.html', context)


def create_file(request, genre_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        form = FileForm(request.POST or None, request.FILES or None)
        genre = get_object_or_404(Genre, pk=genre_id)
        if form.is_valid():
            genre_files = genre.file_set.all()
            for s in genre_files:
                if s.file_name == form.cleaned_data.get("file_name"):
                    context = {
                        'genre': genre,
                        'form': form,
                        'error_message': 'You already added that file',
                    }
                    return render(request, 'upload/file_form.html', context)
            file = form.save(commit=False)
            file.user = request.user
            file.genre = genre
            file.file = request.FILES['file']
            file_type = file.file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'genre': genre,
                    'form': form,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, 'upload/file_form.html', context)

            file.save()
            return render(request, 'upload/detail.html', {'genre': genre})
        context = {
            'genre': genre,
            'form': form,
        }
        return render(request, 'upload/file_form.html', context)


def update_folder(request, genre_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        genre = get_object_or_404(Genre, pk=genre_id)
        if request.POST:
            form = GenreForm(request.POST or None, request.FILES or None, instance=genre)
            if form.is_valid():
                form.genre_image = request.FILES['genre_image']
                file_type = genre.genre_image.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    context = {
                        'genre': genre,
                        'form': form,
                        'error_message': 'Image file must be PNG, JPG, or JPEG',
                    }
                    return render(request, 'upload/update_folder.html', context)
                form.save()
                gen = Genre.objects.all()
                context = {
                    "genre": gen
                }
                return render(request, 'upload/index.html', context)
            else:
                genre = Genre.objects.get(pk=genre_id)
                form = GenreForm(request.POST, instance=genre)
                context = {
                    "form": form,
                }
                return render(request, 'upload/update_folder.html', context)


def rename_file(request, genre_id, file_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        genre = get_object_or_404(Genre, pk=genre_id)
        file = File.objects.get(pk=file_id)
        data = {
            'file_name': file.file_name,
            'file': file.file,
        }
        if request.POST:
            form = FileForm(request.POST or None, request.FILES or None, initial=data)
            if form.is_valid():
                user = request.user
                user.file_name = request.POST['file_name']
                user.save()
                context = {
                    "genre": genre,
                }
                return render(request, 'upload/detail.html', context)
            else:
                file = File.objects.get(pk=file_id)
                form = FileForm(request.POST, instance=file)
                context = {
                    "form": form,
                }
                return render(request, 'upload/update_file.html', context)
        form = FileForm(request.POST or None, request.FILES or None, instance=genre, initial=data)
        context = {
            "genre": genre,
            'form': form,
        }
        return render(request, 'upload/update_file.html', context)


def delete_folder(request, genre_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        genre = get_object_or_404(Genre, pk=genre_id)
        genre.delete()
        gen = Genre.objects.all()
        return render(request, 'upload/index.html', {'genre': gen})


def delete_file(request, genre_id, file_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        genre = get_object_or_404(Genre, pk=genre_id)
        file = File.objects.get(pk=file_id)
        file.delete()
        return render(request, 'upload/detail.html', {'genre': genre})


def files_delete(request, file_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        file = File.objects.get(pk=file_id)
        file.delete()
        fil = File.objects.all()
        return render(request, 'upload/files.html', {'genre_all': fil})


def detail(request, genre_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = request.user
        genre = get_object_or_404(Genre, pk=genre_id)
        return render(request, 'upload/detail.html', {'genre': genre, 'user': user})


def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        genre = Genre.objects.filter(user=request.user)
        file_results = File.objects.all()
        query = request.GET.get("q")
        if query:
            genre = genre.filter(
                Q(genre_name__icontains=query)
            ).distinct()
            file_results = file_results.filter(
                Q(file_name__icontains=query)
            ).distinct()
            return render(request, 'upload/index.html', {
                'genre': genre,
                'files': file_results,
            })
        return render(request, 'upload/index.html', {'genre': genre})


def files(request, filter_by):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        try:
            file_ids = []
            for genre in Genre.objects.filter(user=request.user):
                for file in genre.file_set.all():
                    file_ids.append(file.pk)
            users_files = File.objects.filter(pk__in=file_ids)
            if filter_by == 'favorites':
                users_files = users_files.filter(is_favorite=True)
        except Genre.DoesNotExist:
            users_files = []
        context = {
            'genre_all': users_files,
            'filter_by': filter_by,
        }
        return render(request, 'upload/files.html', context)


def folders(request, filter_by):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        try:
            genre_ids = []
            for genre in Genre.objects.filter(user=request.user):
                genre_ids.append(genre.pk)
            users_genres = Genre.objects.filter(pk__in=genre_ids)
            if filter_by == 'favorites':
                users_genres = users_genres.filter(is_favorite=True)
        except Genre.DoesNotExist:
            users_genres = []
        context = {
            'genre': users_genres,
            'filter_by': filter_by,
        }
        return render(request, 'upload/folders.html', context)


def profile_settings(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'upload/profile_settings.html')


def favorite_file(request, genre_id, file_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        file = get_object_or_404(File, pk=file_id)
        if file.is_favorite:
            file.is_favorite = False
        else:
            file.is_favorite = True
        file.save()
        user = request.user
        genre = get_object_or_404(Genre, pk=genre_id)
        return render(request, 'upload/detail.html', {'genre': genre, 'user': user})


def favorite_folder(request, genre_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        genre = get_object_or_404(Genre, pk=genre_id)
        if genre.is_favorite:
            genre.is_favorite = False
        else:
            genre.is_favorite = True
        genre.save()
        return HttpResponseRedirect('/app/folders/')
