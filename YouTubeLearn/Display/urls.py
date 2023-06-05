from django.urls import path
from Display.views import show_video
from Display.views import send_api_key
from Display.views import create_models
from Display.views import home
from Display.views import playlist                                                                      
from Display.views import delete_playlist
from Display.views import delete_video
from Display.views import add_text

app_name = 'Display'

urlpatterns  = [
    path('videos/<path:name>/', show_video, name='show_video'),
    path('send_api_key/', send_api_key, name='send_api_key'),
    path('create_models/', create_models, name='create_models'),
    path('', home, name='home'),
    path('playlist/<str:name>/', playlist, name='show_playlist'),
    path('delete_playlist/<path:name>/', delete_playlist, name='delete_playlist'),
    path('delete_video/<path:name>/', delete_video, name='delete_video'),
    path('add_text/', add_text, name='add_text'),
    
]