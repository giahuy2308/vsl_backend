from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

# It's required to import Page after creating CustomUser
from communities.models import Page
    
class Notification(models.Model):
    title = models.CharField(max_length=100,default="")
    description = models.TextField()
    user = models.OneToOneField(CustomUser,related_name="notifications",on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100,
        choices=(
            ("Read","read"),
            ("Unread","unread"),
        ),
        default="Unread"
    )
    type = models.CharField(
        max_length=100,
        choices=(
            ("Comment","comment"),
            ("Reaction","reaction"),
            ("Amin","admin"),
            ("Others","others"),
        ),
        default="Others"
    )

    From = models.ForeignKey(Page,related_name="notifications",on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.From is not None:
            return f'{self.title} from {self.From}'
        return f'{self.title}'