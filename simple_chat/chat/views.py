from dataclasses import dataclass
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Message


logger = logging.getLogger("django")


@dataclass
class FormattedMessage:
    username: str
    datetime: str
    text: str


def index(request, warning=None):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    messages = Message.objects.all().select_related()
    datetime_format = "%d.%m, %H:%M"
    formatted_messages = [
        FormattedMessage(
            username=message.user.username,
            datetime=message.datetime.strftime(datetime_format),
            text=message.text,
        )
        for message in messages
    ]
    context = {
        "messages": formatted_messages,
        "logged_username": username,
        "warning": warning,
    }
    return render(request, "chat/index.html", context)

@login_required
def send_message(request):
    message_text = request.POST["message"]

    user = request.user

    new_message = Message(text=message_text, user=user)
    new_message.save()

    logger.log(21, new_message)

    return HttpResponseRedirect(reverse("index"))

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        try:
            if User.objects.get(username=username):
                return HttpResponseRedirect(reverse("index", kwargs={"warning": "Wrong password!"}))
        except User.DoesNotExist:
            pass
        new_user = User.objects.create_user(username=username, password=password)
        new_user.save()
        login(request, new_user)
    return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
