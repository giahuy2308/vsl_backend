from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserQuestion)
admin.site.register(AnswerForUQ)
admin.site.register(Lesson)
admin.site.register(Examination)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Section)
admin.site.register(Exercise)
# admin.site.register(MyAnswer)
admin.site.register(Content)
admin.site.register(Animation)
admin.site.register(Image)