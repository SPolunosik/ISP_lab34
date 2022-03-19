from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test

from .views import show_home, send


def check_user(command):
    return user_passes_test(lambda u: u.is_superuser)(command)


urlpatterns = [
    url(r'^home/$', check_user(show_home), name='home'),
    url(r'^home/send', check_user(send), name='send'),
]
