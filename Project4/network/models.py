from django.contrib.auth.models import AbstractUser
from django.db import models

# ForeignKey = Many-to-One Relationship

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name="followers")
    # symmetrical=False; user A follows user B does not mean that user B also follows user A
    
    def __str__(self):
        return self.username

    def has_liked(self, post):
        return Like.objects.filter(owner=self, post=post).exists()
    
class Post(models.Model):
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"post:'{self.id}', user: '{self.owner}'"

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments") # a user can have muliple comments
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.owner} on {self.post}'

class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.owner} likes {self.post}'


