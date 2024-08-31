from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Section)
admin.site.register(Content)
admin.site.register(Image)
admin.site.register(Animation)
admin.site.register(Exercise)
admin.site.register(Examination)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Assignment)
admin.site.register(UserChoice)
admin.site.register(UserQuestion)
admin.site.register(AnswerForUQ)
