from rest_framework import serializers
from .models import *


class UserQuestionSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = UserQuestion
        fields = (
            'id',
            'content',
            'author',
        )


class AnswerForUQSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = AnswerForUQ
        fields = (
            'id',
            'question',
            'author',
            'content',
        )



class ExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = (
            "id",
            'title',
            'of_course',
            'total_mark',
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "id",
            'examination',
            'title',
            'answer',
        )


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = (
            'id',
            'question',
            'title',
        )


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
            'of_course',
            'status',
        )


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'lesson',
        )


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = (
            'id',
            'lesson',
            'title',
            'content',
            'answer',
        )


# class MyAnswerSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = MyAnswer
    #     fields = (
    #         'exercise',
    #         'author',
    #         'answer',
    #     )
    #     extra_kwargs = {
    #         "author" : {
    #             "read_only":True
    #         }
    #     }


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            'id',
            'section',
            'content',
            'no',
        )


class AnimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = (
            'id',
            'section',
            'name',
            'no',
        )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'id',
            'section',
            'image',
            'alt',
            'no',
        )