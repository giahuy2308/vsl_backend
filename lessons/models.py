from django.contrib.auth import get_user_model 
from django.contrib.postgres.fields import ArrayField
from django.db import models
import os


class Course(models.Model):
    title = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.id}"


class Lesson(models.Model):
    title = models.TextField(max_length=500,default="")
    course = models.ForeignKey(Course, related_name="lessons",on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100,
        choices=(
            ("Completed","completed"),
            ("In Progress","in progress"),
            ("Uncompleted","uncompleted"),
        ),
        default='uncompleted'
    )

    def __str__(self):
        return f"{self.id}"


class Section(models.Model):
    title = models.TextField(max_length=255, default="")
    lesson = models.ForeignKey(Lesson,related_name="sections",on_delete=models.CASCADE)
    content_quantity = models.PositiveIntegerField(default=0)
    content_list = []

    def __str__(self):
        return f"{self.id}"


class Content(models.Model):
    section = models.ForeignKey(Section,related_name="contents",on_delete=models.CASCADE)
    content = models.TextField()
    no = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.no} | {f"{self.id}"}'
    

class Image(models.Model):
    section = models.ForeignKey(Section,related_name="images",on_delete=models.CASCADE)
    alt = models.CharField(max_length=100,default="")
    image = models.ImageField(upload_to="static/image/")
    no = models.PositiveIntegerField(default=1)

    def delete(self):
        remove = super().delete()
        os.remove(self.image.path)        
        return remove

    def __str__(self):
        return f'{self.no} | "{f"{self.id}"}"'


class Animation(models.Model):
    section = models.ForeignKey(Section,related_name="animations",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default="")
    args = ArrayField(models.CharField(max_length=100, blank=True, null=True), blank=True, null=True)
    no = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.no} | "{f"{self.id}"}"'
    

class Exercise(models.Model):
    title = models.TextField(max_length=500, default="")
    content = models.TextField()
    answer = models.TextField()
    lesson = models.ForeignKey(Lesson,related_name="exercises",on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id}"
 

class Examination(models.Model):
    title = models.CharField(max_length=100,default='')
    lesson = models.ForeignKey(Lesson,related_name="examinations", on_delete=models.CASCADE)
    total_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.id}" 


class Question(models.Model):
    examination = models.ForeignKey(Examination,related_name='questions',on_delete=models.CASCADE)
    title = models.TextField(max_length=500,default='')
    answer = models.CharField(max_length=100,default='')
        
    def __str__(self):
        return f"{self.id}"


class Choice(models.Model):
    question = models.ForeignKey(Question,related_name='choices',on_delete=models.CASCADE) 
    title = models.CharField(max_length=500,default='')

    def __str__(self):
        return f"{self.id}"


class Assignment(models.Model):
    author = models.ForeignKey(get_user_model(),related_name="assignment",on_delete=models.CASCADE)
    examination = models.ForeignKey(Examination,related_name="examassiggnment",on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"


class UserChoice(models.Model):
    assignment = models.ForeignKey(Assignment, related_name="userchoices", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="userchoices", on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name="userchoices", on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.id}"


class UserQuestion(models.Model):
    content = models.TextField()
    author = models.ForeignKey(get_user_model(),related_name='questions',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"


class AnswerForUQ(models.Model):
    question = models.ForeignKey(UserQuestion, related_name="answers", on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(),related_name="answers", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
    
