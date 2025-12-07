from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CarpoolPost(models.Model):
    VISIBILITY_CHOICES = [
        ('all', 'All Users'),
        ('drivers', 'Drivers Only'),
        ('riders', 'Riders Only'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, max_length=100)
    name = models.TextField(default="", blank=False)
    dropoff = models.TextField(default="",blank=False)
    pickup = models.TextField(default="", blank=False)
    date = models.TextField(default="", blank=False)
    notes = models.TextField(default="", blank=True)
    pickup_time = models.TimeField()
    dropoff_time = models.TimeField()
    image = models.ImageField(upload_to='carpool_posts/', blank=True, null=True)
    image_visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='all')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.username} - {self.text[:50]}"
    
class Flag(models.Model):
    FLAG_REASONS = [
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam or Misleading'),
        ('safety', 'Safety Concern'),
        ('other', 'Other'),
    ]

    post = models.ForeignKey(CarpoolPost, on_delete=models.CASCADE, related_name='flags')
    flagged_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=FLAG_REASONS, default='other')
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'flagged_by')  # Prevent duplicate flags

    def __str__(self):
        return f"{self.flagged_by.username} flagged {self.post.id} ({self.reason})"

class Review(models.Model):
    post = models.ForeignKey(CarpoolPost, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'reviewer')  # Prevent duplicate reviews
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reviewer.username} -> {self.driver.username} ({self.rating}/5)"