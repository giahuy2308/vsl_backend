from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Community(models.Model):
    name = models.CharField(max_length=100,default="")
    introduction = models.TextField()
    administrator = models.ForeignKey(get_user_model(),related_name="communities_ad", on_delete=models.CASCADE)
    p_password = models.CharField(max_length=200,default="")
    participant = models.ManyToManyField(get_user_model(),related_name="communities_pa")
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.administrator.username}'


class Reaction(models.Model):
    TYPE_CHOICES = (
        ("Like", 'like'),
        ("Haha", 'haha'),
    )
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type',"object_id")
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    author = models.ForeignKey(get_user_model(), related_name="reactions", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} | {self.content_type.model} | {self.object_id}'


class Page(models.Model):
    community = models.ForeignKey(Community,related_name="pages",on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(),related_name="pages",on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="static/image/",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reactions = GenericRelation(Reaction, related_query_name='page')

    def __str__(self):
        return f'Page of {self.author.username} | {self.id}'


class Comment(models.Model):
    page = models.ForeignKey(Page,related_name="comments",on_delete=models.CASCADE) 
    content = models.TextField()
    author = models.ForeignKey(get_user_model(),related_name="comments",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reactions = GenericRelation(Reaction, related_query_name='comment')

    def __str__(self):
        return f'Comment of {self.author.username} | {self.id}'