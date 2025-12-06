from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.decorators.http import require_POST
from dashboard.models import CarpoolPost
from .models import RideRequest

@login_required
@require_POST
def request_ride(request, post_id):
    post = get_object_or_404(CarpoolPost, id=post_id)
    message = request.POST.get('message', '')
    
    # Check if user is a rider
    if request.user.user_type != 'rider':
        messages.error(request, 'Only riders can request rides.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # Create or update ride request
    ride_request, created = RideRequest.objects.get_or_create(
        post=post,
        rider=request.user,
        defaults={
        'message': message,
        'is_seen_by_driver': False,
        'is_seen_by_rider': True}
    )
    
    if created:
        messages.success(request, 'Ride request sent successfully!')
    else:
        messages.info(request, 'You have already requested this ride.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def manage_requests(request, post_id):
    post = get_object_or_404(CarpoolPost, id=post_id, author=request.user)
    requests = RideRequest.objects.filter(post=post, rider__is_active=True)
    
    RideRequest.objects.filter(post=post, is_seen_by_driver=False).update(is_seen_by_driver=True)

    return render(request, 'ride_requests/manage_requests.html', {
        'post': post,
        'requests': requests,
    })

@login_required
@require_POST
def update_request_status(request, request_id):
    ride_request = get_object_or_404(RideRequest, id=request_id, post__author=request.user)
    status = request.POST.get('status')
    
    if status in ['approved', 'rejected']:
        ride_request.status = status

        ride_request.is_seen_by_driver = True
        if status == 'approved':
            ride_request.is_seen_by_rider = False

        ride_request.save()
        messages.success(request, f'Request {status} successfully!')
    
    return redirect('ride_requests:manage_requests', post_id=ride_request.post.id)

@login_required
@require_POST
def cancel_request(request, request_id):
    ride_request = get_object_or_404(RideRequest, id=request_id, rider=request.user)

    ride_request.is_seen_by_driver = True
    ride_request.save()

    ride_request.delete()
    messages.success(request, 'Ride request cancelled successfully!')
    return redirect(request.META.get('HTTP_REFERER', '/'))