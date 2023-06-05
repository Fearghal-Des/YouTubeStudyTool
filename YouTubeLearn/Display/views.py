from django.shortcuts import render, redirect
from django.http import JsonResponse
from decouple import Config, RepositoryEnv
from Display.models import Video, Playlist

config = Config(RepositoryEnv('.env'))
api_key = config('API_KEY')
                  

def show_video(request, name):
    try:
        video = Video.objects.get(name=name)
        video_id = video.url.split('=')[1]  # Extract the video ID from the URL#  
        if '&' in video_id:
            video_id = video.url.split('&')[0] 
        print(video.words)
        context = {
            'video_id': video_id,
            'name': name,
            'words': video.words,
        }
        print(video.words)
        return render(request, 'Display/youtube.html', context)
    except Video.DoesNotExist:
        print('Video does not exist')
        return redirect('Display:home')
    except Video.MultipleObjectsReturned:
        print('Multiple videos returned')
        return redirect('Display:home')
    except:
        print('Something else went wrong')
        return redirect('Display:home')


def send_api_key(request):
    if request.method == 'GET':
        return JsonResponse({'api_key_response': api_key})
    
def home(request):
    videos = Video.objects.exclude(_inherited=True)[:10]
    playlists = Playlist.objects.all()[:10]

    context = {
        'videos': videos,
        'playlists': playlists,
    }

    return render(request, 'Display/youhome.html', context)
    
def create_models(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            if url in [video.url for video in Video.objects.all()]:
                return redirect('Display:home')
            if url in [playlist.url for playlist in Playlist.objects.all()]:
                return redirect('Display:home')
            # Check if the URL is for a video or a playlist
            if 'youtube.com/playlist' in url:
                # Create Playlist model
                playlist = Playlist(url=url)
                playlist.save()
            elif 'youtube.com/watch' in url:
                # Create Video model
                video = Video(url=url)
                video.save()
                if video.name == None:
                    video.name = video.url.split('=')[1]
                    return redirect('Display:home')

    # Redirect back to the same page after creating the models
    return redirect('Display:home')


def playlist(request, name):
    playlist = Playlist.objects.get(name=name)
    return render(request, 'Display/youplaylist.html', {'playlist': playlist}) 


def delete_video(request, name):
    if request.method == 'POST':
        video = Video.objects.get(name=name)
        video.delete()
        return redirect('Display:home')
    else:
        return redirect('Display:home')
    
def delete_playlist(request, name):
    if request.method == 'POST':
        playlist = Playlist.objects.get(name=name)
        playlist.delete()
        return redirect('Display:home')
    else:
        return redirect('Display:home')
    

def add_text(request):
    if request.method == 'POST':
        print('message received')
        text = request.POST.get('text')
        name = request.POST.get('name')
        video = Video.objects.get(name=name)
        video.words = text
        print(video.words)
        video.save()
        return redirect('Display:show_video', name=name)
    else:
        return redirect('Display:show_video', name=name)