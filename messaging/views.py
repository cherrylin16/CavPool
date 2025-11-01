from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def message_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "messaging/message_list.html", {"users": users})


@login_required
def chat_room(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    return render(request, "messaging/message_detail.html", {"other_user": other_user})


@login_required
def new_message(request):
    return redirect("message_page")