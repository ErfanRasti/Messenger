"""This file manages the html files for the chat app."""

# Importing libraries
from django.shortcuts import render
from django.contrib.auth import get_user_model
from chat.models import ChatModel

# Create your views here.

# Creating an object of the user model

user = get_user_model()


def index(request):
    """Render the index.html file and exclude the current user."""
    users = user.objects.exclude(username=request.user.username)
    return render(request, "index.html", context={"users": users})


def chatPage(request, username):
    """Render the main_chat.html file and exclude the current user."""
    user_obj = user.objects.get(username=username)
    users = user.objects.exclude(username=request.user.username)

    if request.user.id > user_obj.id:
        thread_name = f"chat_{request.user.id}-{user_obj.id}"
    else:
        thread_name = f"chat_{user_obj.id}-{request.user.id}"
    message_objs = ChatModel.objects.filter(thread_name=thread_name)
    return render(
        request,
        "main_chat.html",
        context={"users": users, "user": user_obj, "message_objs": message_objs},
    )
