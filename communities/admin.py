from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Community)
admin.site.register(CommunityRule)
admin.site.register(Participant)
admin.site.register(JoinInRequest)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reaction)