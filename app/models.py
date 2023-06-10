from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

'''
By default, Django's User model does not include a profile attribute with a description field. 
However, it's a common practice to extend the User model with a separate Profile model to add 
additional fields and information specific to each user.

To achieve this, you would need to create a separate Profile model and link it to the User 
model using a one-to-one relationship. Here's an example of how you can extend the User model 
with a Profile model:
'''

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs')

    def __str__(self):
        return f"Blog by {self.user.username}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog}"
