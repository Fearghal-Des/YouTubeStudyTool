from django import forms
from .models import Video, Playlist
from django.forms import ModelForm

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = '__all__'
        
class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields = '__all__'