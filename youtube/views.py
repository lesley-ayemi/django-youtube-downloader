from django.shortcuts import render, redirect
from django.contrib import messages
from pytube import YouTube
import certifi
import urllib3
from django.http import JsonResponse

# Create your views here.
def home(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    
    if request.method == 'POST':
        get_link = request.POST['get_link']

        try:
            # Set the CA certificates using certifi
            certifi.where()
            
            yt = YouTube(get_link)
            video_stream = yt.streams.filter(file_extension='mp4').first()
            file_size = video_stream.filesize
            
            # Define a callback function to update progress
            def progress_callback(chunk, file_handle, bytes_remaining):
                percent = (float(file_size - bytes_remaining) / float(file_size)) * 100.0
                return JsonResponse({'percent': percent})
            
            # Download the video with the progress callback
            video_stream.download(callback=progress_callback)
            # video_stream.download()

            messages.success(request, 'Downloading Successful')
            print('success')
            return redirect('home')
        except Exception as e:
            messages.warning(request, f'Failed to download video: {str(e)}')
            print(f'Failed to download video: {str(e)}')
            return redirect('home')
    else:
        return redirect('home')

