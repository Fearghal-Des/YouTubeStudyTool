from googleapiclient.discovery import build
from django.db import models

from decouple import Config, RepositoryEnv

import random
import string
from ckeditor.fields import RichTextField

config = Config(RepositoryEnv('.env'))
api_key = config('API_KEY')


class Video(models.Model):
    url = models.URLField()
    thumbnail = models.URLField(null=True, blank=True)  # Add the thumbnail field
    name = models.CharField(max_length=200, null=True, blank=True)  # Add the name field
    _inherited = models.BooleanField(default=False)
    words = RichTextField(default='')  # Add the words field

    def save(self, *args, **kwargs):
        video_id = self.url.split('=')[1]
        if '&' in video_id:
            video_id = video_id.split('&')[0]
        self.thumbnail = get_video_thumbnail(video_id)  # Set the thumbnail before saving
        self.name = get_video_name(video_id) # Set the name before saving
        super().save(*args, **kwargs)
        
    @property
    def model_name(self):
        return 'Video'

    def __str__(self):
        return self.url


class Playlist(models.Model):
    url = models.URLField()
    thumbnail = models.URLField(null=True, blank=True)  # Add the thumbnail field
    name = models.CharField(max_length=200, null=True, blank=True)  # Add the name field
    videos = models.ManyToManyField(Video, related_name='playlists')  # Add the videos field

    def save(self, *args, **kwargs):
        playlist_id = self.url.split('=')[1]
        # convert_playlist_to_videos(playlist_id)
        self.thumbnail = get_playlist_thumbnail(playlist_id)
        self.name = get_playlist_name(playlist_id)
        super().save(*args, **kwargs)  # Save the Playlist instance to the database
        self.videos.set(get_videos(playlist_id, self))  # Set the many-to-many relationship



    @property
    def model_name(self):
        return 'Playlist'
    
    def __str__(self):
        return self.url

def get_playlist_thumbnail(playlist_id):
    # Use the YouTube Data API client to retrieve the playlist thumbnail
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.playlists().list(
        part='snippet',
        id=playlist_id
    )
    response = request.execute()

    # Extract the playlist thumbnail URL from the response
    if 'items' in response and len(response['items']) > 0:
        playlist_snippet = response['items'][0]['snippet']
        if 'thumbnails' in playlist_snippet:
            thumbnails = playlist_snippet['thumbnails']
            if 'medium' in thumbnails:
                return thumbnails['medium']['url']

    return None


def get_video_thumbnail(video_id):
    # Use the YouTube Data API client to retrieve the video thumbnail
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    response = request.execute()

    # Extract the video thumbnail URL from the response
    if 'items' in response and len(response['items']) > 0:
        video_snippet = response['items'][0]['snippet']
        if 'thumbnails' in video_snippet:
            thumbnails = video_snippet['thumbnails']
            if 'medium' in thumbnails:
                return thumbnails['medium']['url']

    return None

def get_video_name(video_id):
    # Use the YouTube Data API client to retrieve the video name
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    response = request.execute()

    # Extract the video name from the response
    if 'items' in response and len(response['items']) > 0:
        video_snippet = response['items'][0]['snippet']
        if 'title' in video_snippet:
            return video_snippet['title']

    return random.choice(string.ascii_letters)

def get_video_response(video_id):
        # Use the YouTube Data API client to retrieve the video name
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    response = request.execute()
    response = response['items']
    return response

def get_playlist_name(playlist_id):
    # Use the YouTube Data API client to retrieve the playlist name
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.playlists().list(
        part='snippet',
        id=playlist_id
    )
    response = request.execute()

    # Extract the playlist name from the response
    if 'items' in response and len(response['items']) > 0:
        playlist_snippet = response['items'][0]['snippet']
        if 'title' in playlist_snippet:
            return playlist_snippet['title']

    return random.choice(string.ascii_letters)

def get_videos(playlist_id, playlist):
    # Set up the YouTube Data API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Retrieve the playlist items
    playlist_items = []
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        playlist_items.extend(response['items'])
        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break


    for item in playlist_items:
        video_id = item['contentDetails']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        video = Video.objects.create(name=get_video_name(video_id), thumbnail=get_video_thumbnail(video_id)
                                           , url=video_url, _inherited=True)
        playlist.videos.add(video)
        
    return playlist.videos.all()