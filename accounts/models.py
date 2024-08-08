from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  
    pass

# It's required to import Page after creating CustomUser
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes.fields import GenericForeignKey  
    
class Notification(models.Model):
    content = models.TextField()
    user = models.ForeignKey(get_user_model(),related_name="user_notif",on_delete=models.CASCADE)
    sender = models.ForeignKey(get_user_model(),related_name="sender_notif",on_delete=models.CASCADE,blank=True,null=True)

    status = models.CharField(
        max_length=100,
        choices=(
            ("Read","read"),
            ("Unread","unread"),
        ),
        default="Unread"
    )

    From = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('From',"object_id")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.sender is not None and self.From is not None:
                return f'{self.user} | {self.From.model} | {self.sender} |'
        elif self.sender is not None and self.From is None:
            return f'{self.user} | ... | {self.sender} |'
        elif self.sender is None and self.From is not None:
            return f'{self.user} | {self.From.model} | ... |'
        return f'{self.user} | ... | ... |'