from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blog by {self.user.username}"