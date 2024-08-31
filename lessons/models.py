from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
import os


class Course(models.Model):
    title = models.CharField(max_length=255, default="")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class ModelWithNo(models.Model):
    title = models.CharField(max_length=255, default="", unique=True)
    no = models.BigIntegerField(default=-1)

    class Meta:
        abstract = True
        ordering = ["no"]

    def __str__(self) -> str:
        return f"{self.no} | {self.id}"


class Topic(ModelWithNo):
    course = models.ForeignKey(Course, related_name="topics", on_delete=models.CASCADE)
    theme_color = models.CharField(max_length=255, default="")


class Chapter(ModelWithNo):
    topic = models.ForeignKey(Topic, related_name="chapters", on_delete=models.CASCADE)
    summary = models.TextField(default="")


class Lesson(ModelWithNo):
    chapter = models.ForeignKey(
        Chapter, related_name="lessons", on_delete=models.CASCADE
    )


class Section(ModelWithNo):
    lesson = models.ForeignKey(
        Lesson, related_name="sections", on_delete=models.CASCADE
    )
    component_quantity = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.no} | {self.id}"


class SectionContentModel(models.Model):
    section = models.ForeignKey(
        Section, related_name="%(class)ss", on_delete=models.CASCADE
    )
    no = models.BigIntegerField(default=-1)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.no} | {self.id}"


class Content(SectionContentModel):
    content = models.TextField()


class Image(SectionContentModel):
    alt = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to="static/image/")
    title = models.CharField(max_length=100, blank=True, null=True)

    def delete(self):
        remove = super().delete()
        os.remove(self.image.path)
        return remove


class Animation(SectionContentModel):
    name = models.CharField(max_length=100, default="")
    args = ArrayField(
        models.CharField(max_length=100, blank=True, null=True), blank=True, null=True
    )


class Exercise(SectionContentModel):
    content = models.TextField()
    answer = models.TextField()


class Examination(models.Model):
    title = models.CharField(max_length=100, default="")
    chapter = models.ForeignKey(
        Chapter, related_name="examinations", on_delete=models.CASCADE
    )
    total_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.id}"


class Question(models.Model):
    examination = models.ForeignKey(
        Examination, related_name="questions", on_delete=models.CASCADE
    )
    title = models.TextField(max_length=500, default="")
    answer = models.CharField(max_length=100, default="")

    class Meta:
        unique_together = (("examination", "title", "answer"),)

    def __str__(self):
        return f"{self.id}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=500, default="")

    class Meta:
        unique_together = (("question", "title"),)

    def __str__(self):
        return f"{self.id}"


class Assignment(models.Model):
    author = models.ForeignKey(
        get_user_model(), related_name="assignment", on_delete=models.CASCADE
    )
    examination = models.ForeignKey(
        Examination, related_name="examassiggnment", on_delete=models.CASCADE
    )
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.id}"


class UserChoice(models.Model):
    assignment = models.ForeignKey(
        Assignment, related_name="userchoices", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question, related_name="userchoices", on_delete=models.CASCADE
    )
    choice = models.ForeignKey(
        Choice,
        related_name="userchoices",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.id}"


class UserQuestion(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
        get_user_model(), related_name="questions", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"


class AnswerForUQ(models.Model):
    question = models.ForeignKey(
        UserQuestion, related_name="answers", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        get_user_model(), related_name="answers", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
