# chat/views.py
from django.shortcuts import render
from django.shortcuts import redirect

def index(request):
    return render(request, 'sock_chat_app/index.html', {})

def redirect_to_index(request):
    response = redirect('sock_chat_app/')
    return response


def room(request, room_name):
    return render(request, 'sock_chat_app/room.html', {
        'room_name': room_name
    })