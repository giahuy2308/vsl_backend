from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Community(models.Model):
    name = models.CharField(max_length=100,default="")
    introduction = models.TextField()
    administrator = models.ForeignKey(get_user_model(),related_name="communities_ad", on_delete=models.CASCADE)
    p_password = models.CharField(max_length=200,default="")
    participant = models.ForeignKey(get_user_model(),related_name="communities_pa",on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.administrator.username}'


class Page(models.Model):
    community = models.ForeignKey(Community,related_name="pages",on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(),related_name="pages",on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="static/image/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Page of {self.author.username}'


class Comment(models.Model):
    page = models.ForeignKey(Page,related_name="comments",on_delete=models.CASCADE) 
    content = models.TextField()
    author = models.ForeignKey(get_user_model(),related_name="comments",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment of {self.author.username}'


class Reaction(models.Model):
    type = models.CharField(
        max_length=100,
        choices=(
            ("Like",'like'),
            ("Haha",'haha'),
        )
    )
    author = models.ForeignKey(get_user_model(),related_name="reactions",on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type}'