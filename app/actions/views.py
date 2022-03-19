from django.shortcuts import render
from ugc.management.commands.handler import send_to_all_user


def send(request):
    send_to_all_user(request.POST.get('message', 'error'))
    return render(request, 'actions/home.html')


def show_home(request):
    ctx = {'data': 'test'}
    return render(request, 'actions/home.html', ctx)
