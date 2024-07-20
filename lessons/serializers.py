from rest_framework import serializers
from .models import *


class UserQuestionSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = UserQuestion
        fields = "__all__"


class AnswerForUQSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = AnswerForUQ
        fields = "__all__"



class ExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


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
        fields = "__all__"


class AnimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"