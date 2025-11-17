from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import RideRequest


@login_required
def driver_unseen_requests(request):
    """
    Count ride requests for rides OWNED by the logged-in driver
    where is_seen_by_driver=False.
    """
    unseen = RideRequest.objects.filter(
        post__author=request.user,
        is_seen_by_driver=False,
        status='pending'
    ).count()

    return JsonResponse({"unseen": unseen})


@login_required
def rider_unseen_approvals(request):
    """
    Count approvals for this rider where is_seen_by_rider=False.
    """
    unseen = RideRequest.objects.filter(
        rider=request.user,
        is_seen_by_rider=False,
        status='approved'
    ).count()
    
    return JsonResponse({"unseen": unseen})