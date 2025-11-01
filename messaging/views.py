from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def message_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "messaging/message_list.html", {"users": users})


@login_required
def message_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    return render(request, "messaging/message_detail.html", {"other_user": other_user})


@login_required
def new_message(request):
    return redirect("message_list")

@login_required
def new_message(request):
    if request.method == "POST":
        username = request.POST.get("username")
        message_text = request.POST.get("message")

        try:
            recipient = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("new_message")

        return redirect("message_detail", username=recipient.username)

    users = User.objects.exclude(id=request.user.id)
    return render(request, "messaging/new_message.html", {"users": users})