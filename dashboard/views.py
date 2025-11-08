from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import RiderProfile, DriverProfile, User
from .models import CarpoolPost
from .forms import CarpoolPostForm
from django.http import JsonResponse
from .models import CarpoolPost, Flag
from django.views.decorators.http import require_POST
from django.db.models import Q
from ride_requests.models import RideRequest

def rider_dashboard(request):
    profile = None
    display_name = request.user.username
    if request.user.is_authenticated:
        try:
            profile = RiderProfile.objects.get(user=request.user)
            if profile.name:
                display_name = profile.name
        except RiderProfile.DoesNotExist:
            pass

     # search queries
    query = request.GET.get('q', '')

    posts = CarpoolPost.objects.all()

    if query:
        posts = posts.filter(
            Q(name__icontains=query) |
            Q(dropoff__icontains=query) |
            Q(pickup__icontains=query) |
            Q(date__icontains=query) |
            Q(pickup_time__icontains=query) |
            Q(dropoff_time__icontains=query) |
            Q(name__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()
    
    flagged_posts = set(Flag.objects.filter(flagged_by=request.user).values_list('post_id', flat=True))
    
    # Get user's ride requests and add them to posts
    user_requests = set()
    if request.user.is_authenticated:
        user_ride_requests = RideRequest.objects.filter(rider=request.user)
        user_requests = set(user_ride_requests.values_list('post_id', flat=True))
        request_dict = {req.post_id: req for req in user_ride_requests}
        
        # Add request object to each post
        for post in posts:
            post.user_request = request_dict.get(post.id)
    
    return render(request, "dashboard/rider_dashboard.html", {
        'display_name': display_name,
        'posts': posts,
        'query': query,
        'flagged_posts': flagged_posts,
        'user_requests': user_requests
    })

def driver_dashboard(request):
    profile = None
    display_name = request.user.username
    if request.user.is_authenticated:
        try:
            profile = DriverProfile.objects.get(user=request.user)
            if profile.name:
                display_name = profile.name
        except DriverProfile.DoesNotExist:
            pass
    
    # search queries
    query = request.GET.get('q', '')

    posts = CarpoolPost.objects.all()

    if query:
        posts = posts.filter(
            Q(name__icontains=query) |
            Q(dropoff__icontains=query) |
            Q(pickup__icontains=query) |
            Q(date__icontains=query) |
            Q(pickup_time__icontains=query) |
            Q(dropoff_time__icontains=query) |
            Q(name__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()


    flagged_posts = set(Flag.objects.filter(flagged_by=request.user).values_list('post_id', flat=True))
    form = CarpoolPostForm()
    return render(request, "dashboard/driver_dashboard.html", {
        'display_name': display_name, 
        'posts': posts, 
        'query': query,
        'form': form,
        'flagged_posts': flagged_posts
    })

@login_required
def create_carpool_post(request):
    if request.method == 'POST':
        # Handle deletion
        if 'delete_post_id' in request.POST:
            post_id = request.POST.get('delete_post_id')
            CarpoolPost.objects.filter(id=post_id, author=request.user).delete()
            messages.success(request, 'Post deleted successfully.')
            return redirect('driver dashboard')

        # Handle creation
        form = CarpoolPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Carpool post created successfully!')
            return redirect('driver dashboard')
        
    return redirect('driver dashboard')

def landing(request):
    return render(request, "dashboard/landing.html")

def moderator_dashboard(request):
    display_name = request.user.username
    return render(request, "dashboard/moderator_dashboard.html", {
        "display_name": display_name
    })

@login_required
def flagged_posts(request):
    if not request.user.is_moderator:
        return redirect('/')
    
    # Get posts that have flags
    flagged_posts = CarpoolPost.objects.filter(flags__isnull=False).distinct().prefetch_related('flags__flagged_by')
    return render(request, "dashboard/flagged_posts.html", {
        "flagged_posts": flagged_posts
    })

@login_required
@require_POST
def moderate_post(request, post_id):
    if not request.user.is_moderator:
        return redirect('/')
    
    post = CarpoolPost.objects.get(id=post_id)
    action = request.POST.get('action')
    
    if action == 'approve':
        # Remove all flags for this post
        Flag.objects.filter(post=post).delete()
        messages.success(request, f'Post approved and all flags removed.')
    elif action == 'delete':
        # Delete the post and its flags
        post.delete()
        messages.success(request, f'Post deleted successfully.')
    
    return redirect('flagged_posts')

@login_required
@require_POST
def flag_post(request, post_id):
    post = CarpoolPost.objects.get(id=post_id)
    reason = request.POST.get('reason', 'other')
    details = request.POST.get('details', '')

    flag, created = Flag.objects.update_or_create(
        post=post,
        flagged_by=request.user,
        defaults={'reason': reason, 'details': details}
    )

    if created:
        messages.success(request, "Post flagged successfully. Our moderators will review it soon.")
    else:
        messages.success(request, "Flag updated successfully. Our moderators will review it soon.")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))