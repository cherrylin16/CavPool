from django.db import models
from django.contrib.auth import get_user_model
from dashboard.models import CarpoolPost

User = get_user_model()

class RideRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    post = models.ForeignKey(CarpoolPost, on_delete=models.CASCADE, related_name='ride_requests')
    rider = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('post', 'rider')  # Prevent duplicate requests
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.rider.username} -> {self.post.author.username} ({self.status})"