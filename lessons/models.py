from django.db import models
from django.contrib.auth import get_user_model 

# Create your models here.


class UserQuestion(models.Model):
    content = models.TextField()
    author = models.ForeignKey(get_user_model(),related_name='questions',on_delete=models.CASCADE)

    def __str__(self):
        return f'Question of "{self.author.username}"'


class AnswerForUQ(models.Model):
    question = models.ForeignKey(UserQuestion, related_name="answers", on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(),related_name="answers", on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'Answer of "{self.author.username}" for "{self.question.author.username}" question'


class Examination(models.Model):
    title = models.CharField(max_length=100,default='')
    of_course = models.CharField(max_length=100,default='')
    # author = models.ForeignKey(get_user_model(),related_name="examinations",on_delete=models.CASCADE)
    total_mark = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'"{self.title}" of "{self.of_course}"'


class Question(models.Model):
    examination = models.ForeignKey(Examination,related_name='questions',on_delete=models.CASCADE)
    title = models.CharField(max_length=100,default='')
    answer = models.CharField(max_length=100,default='')

    def __str__(self):
        return f'"{self.title}" of "{self.examination.title}"'


class Choice(models.Model):
    question = models.ForeignKey(Question,related_name='choices',on_delete=models.CASCADE) 
    title = models.CharField(max_length=100,default='')

    def __str__(self):
        return f'"{self.title}" of "{self.question.title}"'


class Lesson(models.Model):
    title = models.CharField(max_length=100,default="")
    of_course = models.CharField(max_length=100,default="")
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
        return f'"{self.title}" of "{self.of_course}"'


class Exercise(models.Model):
    title = models.CharField(max_length=100, default="")
    content = models.TextField()
    answer = models.TextField()
    lesson = models.ForeignKey(Lesson,related_name="exercises",on_delete=models.CASCADE)
    
    def __str__(self):
        return f'"{self.title}" of "{self.lesson.title}"'


# class MyAnswer(models.Model):
    # answer = models.TextField()
    # exercise = models.ForeignKey(Exercise, related_name="myanswers", on_delete=models.CASCADE)
    # author = models.ForeignKey(get_user_model(), related_name="myanswers",on_delete=models.CASCADE) 

    # def __str__(self):
    #     return f'answer of "{self.author.username}" for "{self.exercise.title}"'


class Section(models.Model):
    title = models.CharField(max_length=100, default="")
    lesson = models.ForeignKey(Lesson,related_name="sections",on_delete=models.CASCADE)
    content_quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.title}"


class Content(models.Model):
    section = models.ForeignKey(Section,related_name="contents",on_delete=models.CASCADE)
    content = models.TextField()
    no = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'"{self.no}" of "{self.section.title}"'
    

class Image(models.Model):
    section = models.ForeignKey(Section,related_name="images",on_delete=models.CASCADE)
    alt = models.CharField(max_length=100,default="")
    image = models.ImageField(upload_to="static/image/")
    no = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'"{self.no}" of "{self.section.title}"'


class Animation(models.Model):
    section = models.ForeignKey(Section,related_name="animations",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default="")
    no = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'"{self.no}" of "{self.section.title}"'