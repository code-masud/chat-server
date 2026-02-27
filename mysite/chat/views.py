from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def index(request):
    users = User.objects.exclude(pk=request.user.id)
    return render(request, "chat/index.html", {'users': users})

@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

@login_required
def private_chat(request, username):
    other_user = get_object_or_404(User, username=username)

    current_user = request.user

    # Create deterministic room name
    users = sorted([current_user.username, other_user.username])
    room_name = f"private_{users[0]}_{users[1]}"

    return render(request, "chat/room.html", {
        "room_name": room_name,
        "other_user": other_user
    })