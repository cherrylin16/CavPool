from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def messages_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "messages/message_list.html", {"users": users})

@login_required
def message_detail(request, username):
    other_user = get_object_or_404(User, username=username)
    return render(request, "messages/message_detail.html", {"other_user": other_user})