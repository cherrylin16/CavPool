from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.decorators import verified_required
from .models import Message
from django.http import JsonResponse

User = get_user_model()

@verified_required
def message_list(request):
    from django.db.models import Q, Max
    
    # Get users who have active conversations with current user
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).values('sender', 'receiver').annotate(
        last_message_time=Max('timestamp')
    ).order_by('-last_message_time')
    
    # Build list of conversation partners with last message
    conversation_data = []
    seen_users = set()
    
    for conv in conversations:
        other_user_id = conv['sender'] if conv['receiver'] == request.user.id else conv['receiver']
        
        if other_user_id not in seen_users and other_user_id != request.user.id:
            seen_users.add(other_user_id)
            other_user = User.objects.get(id=other_user_id)
            
            # Get the last message between these users
            last_message = Message.objects.filter(
                Q(sender=request.user, receiver=other_user) |
                Q(sender=other_user, receiver=request.user)
            ).order_by('-timestamp').first()
            
            conversation_data.append({
                'user': other_user,
                'last_message': last_message
            })
    
    return render(request, "messaging/message_list.html", {"conversations": conversation_data})

@login_required
def unread_count(request):
    count = Message.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({"unread": count})

@verified_required
def message_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=message_text
            )
        return redirect("message_detail", user_id=user_id)

    messages_qs = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    return render(request, "messaging/message_detail.html", {
        "other_user": other_user,
        "messages": messages_qs
    })


@verified_required
def new_message(request):
    if request.method == "POST":
        username = request.POST.get("username")
        message_text = request.POST.get("message")

        try:
            recipient = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("new_message")

        # Create the message
        Message.objects.create(
            sender=request.user,
            receiver=recipient,
            content=message_text
        )

        return redirect("message_detail", user_id=recipient.id)

    users = User.objects.exclude(id=request.user.id)
    return render(request, "messaging/new_message.html", {"users": users})