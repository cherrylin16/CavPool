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
from datetime import datetime, date, time

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

     # search queries and filters
    query = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    pickup_time_filter = request.GET.get('pickup_time', '')
    dropoff_time_filter = request.GET.get('dropoff_time', '')

    posts = CarpoolPost.objects.filter(author__is_active=True)

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
    
    if date_filter:
        posts = posts.filter(date__icontains=date_filter)
    
    if pickup_time_filter:
        posts = posts.filter(pickup_time__icontains=pickup_time_filter)
    
    if dropoff_time_filter:
        posts = posts.filter(dropoff_time__icontains=dropoff_time_filter)
    
    # Separate active and previous posts
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    
    active_posts = []
    previous_posts = []
    
    for post in posts:
        try:
            # Parse date and time from post
            post_date = datetime.strptime(post.date, '%Y-%m-%d').date()
            post_time = datetime.strptime(post.pickup_time, '%H:%M').time()
            
            # Check if post is in the future
            if post_date > current_date or (post_date == current_date and post_time > current_time):
                active_posts.append(post)
            else:
                previous_posts.append(post)
        except (ValueError, TypeError):
            # If date/time parsing fails, treat as active
            active_posts.append(post)
    
    flagged_posts = set(Flag.objects.filter(flagged_by=request.user).values_list('post_id', flat=True))
    
    # Get user's ride requests and add them to posts
    user_requests = set()
    if request.user.is_authenticated:
        user_ride_requests = RideRequest.objects.filter(rider=request.user, rider__is_active=True)
        user_requests = set(user_ride_requests.values_list('post_id', flat=True))
        request_dict = {req.post_id: req for req in user_ride_requests}
        
        # Add request object to each post
        for post in active_posts + previous_posts:
            post.user_request = request_dict.get(post.id)
    
    return render(request, "dashboard/rider_dashboard.html", {
        'display_name': display_name,
        'active_posts': active_posts,
        'previous_posts': previous_posts,
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
    
    # search queries and filters
    query = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    pickup_time_filter = request.GET.get('pickup_time', '')
    dropoff_time_filter = request.GET.get('dropoff_time', '')

    posts = CarpoolPost.objects.filter(author__is_active=True)

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
    
    if date_filter:
        posts = posts.filter(date__icontains=date_filter)
    
    if pickup_time_filter:
        posts = posts.filter(pickup_time__icontains=pickup_time_filter)
    
    if dropoff_time_filter:
        posts = posts.filter(dropoff_time__icontains=dropoff_time_filter)

    # Separate active and previous posts
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    
    active_posts = []
    previous_posts = []
    
    for post in posts:
        try:
            # Parse date and time from post
            post_date = datetime.strptime(post.date, '%Y-%m-%d').date()
            post_time = datetime.strptime(post.pickup_time, '%H:%M').time()
            
            # Check if post is in the future
            if post_date > current_date or (post_date == current_date and post_time > current_time):
                active_posts.append(post)
            else:
                previous_posts.append(post)
        except (ValueError, TypeError):
            # If date/time parsing fails, treat as active
            active_posts.append(post)

    flagged_posts = set(Flag.objects.filter(flagged_by=request.user).values_list('post_id', flat=True))
    form = CarpoolPostForm()
    return render(request, "dashboard/driver_dashboard.html", {
        'display_name': display_name, 
        'active_posts': active_posts,
        'previous_posts': previous_posts,
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

@login_required
def ban_user(request):
    if not request.user.is_moderator:
        return redirect('/')
    
    search_query = request.GET.get('search', '')
    user_found = None
    has_driver_profile = False
    has_rider_profile = False
    user_type_display = 'None'
    
    if search_query:
        try:
            # First try exact username match, then email match
            user_found = User.objects.filter(username__iexact=search_query).first()
            if not user_found:
                user_found = User.objects.filter(email__iexact=search_query).first()
            
            if user_found:
                driver_profiles = DriverProfile.objects.filter(user=user_found)
                rider_profiles = RiderProfile.objects.filter(user=user_found)
                
                has_driver_profile = driver_profiles.exists()
                has_rider_profile = rider_profiles.exists()
                
                # If no actual profiles exist but user_type is set, treat as if profile exists for deletion purposes
                if not has_driver_profile and user_found.user_type == 'driver':
                    has_driver_profile = True
                if not has_rider_profile and user_found.user_type == 'rider':
                    has_rider_profile = True
                
                # Create display string for user types
                user_types = []
                if has_driver_profile:
                    user_types.append('Driver')
                if has_rider_profile:
                    user_types.append('Rider')
                user_type_display = ' and '.join(user_types) if user_types else 'None'
        except Exception:
            pass
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        profile_type = request.POST.get('profile_type')
        
        try:
            target_user = User.objects.get(id=user_id)
            
            if profile_type == 'driver':
                try:
                    target_user.driverprofile.delete()
                except DriverProfile.DoesNotExist:
                    pass
                messages.success(request, f'Driver profile for {target_user.username} has been deleted.')
            elif profile_type == 'rider':
                try:
                    target_user.riderprofile.delete()
                except RiderProfile.DoesNotExist:
                    pass
                messages.success(request, f'Rider profile for {target_user.username} has been deleted.')
            
            # Check if user has any remaining profiles
            has_driver = DriverProfile.objects.filter(user=target_user).exists()
            has_rider = RiderProfile.objects.filter(user=target_user).exists()
            
            # Always clear the user_type for the deleted profile type
            if profile_type == 'driver':
                if has_rider:
                    target_user.user_type = 'rider'
                else:
                    target_user.user_type = None
            elif profile_type == 'rider':
                if has_driver:
                    target_user.user_type = 'driver'
                else:
                    target_user.user_type = None
            
            # If no profiles left, deactivate account
            if not has_driver and not has_rider:
                target_user.username = f"[deleted]_{target_user.id}"
                target_user.email = f"deleted_{target_user.id}@deleted.com"
                target_user.is_active = False
                messages.success(request, f'User account has been completely deactivated.')
            
            target_user.save()
            
        except Exception as e:
            messages.error(request, f'Error deleting profile: {e}')
        
        return redirect('ban_user')
    
    return render(request, 'dashboard/ban_user.html', {
        'search_query': search_query,
        'user_found': user_found,
        'has_driver_profile': has_driver_profile,
        'has_rider_profile': has_rider_profile,
        'user_type_display': user_type_display,
    })