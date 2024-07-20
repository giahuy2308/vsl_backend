from rest_framework import viewsets, permissions, views, status
from django.http import Http404
# import requests
from .models import *
from .serializers import *
from .permissions import *

# Create your views here.

class UserQuestionView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsAuthorOrReadOnly]
    serializer_class = UserQuestionSerializer
    queryset = UserQuestion.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerForUQView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsAuthorOrReadOnly]
    serializer_class = AnswerForUQSerializer
    queryset = AnswerForUQ.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ExaminationView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = ExaminationSerializer
    queryset = Examination.objects.all()

    # def list(self, request):
    #     examinations = Examination.objects.all()
    #     serializer = ExaminationSerializer(examinations, many=True)
    #     for i in range(len(examinations)):
    #         questions = QuestionSerializer(examinations[i].questions.all(), many=True).data
    #         serializer.data[i]["examinations"] = questions
    #         for j in range(len(questions)):
    #             choices = ChoiceSerializer(Question.objects.get(pk=questions[j]['id']).choices.all(), many=True).data
    #             serializer.data[i]["examinations"][j]["choices"] = choices
    #     return views.Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        examination = self.get_object()
        serializer = ExaminationSerializer(examination)
        questions = QuestionSerializer(examination.questions.all(), many=True).data
        data = serializer.data
        data["examinations"] = questions
        for j in range(len(questions)):
            choices = ChoiceSerializer(Question.objects.get(pk=questions[j]['id']).choices.all(), many=True).data
            data["examinations"][j]["choices"] = choices
        return views.Response(data, status=status.HTTP_200_OK)


class QuestionView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        answer = Choice.objects.create(title=serializer.data["answer"], question=Question.objects.get(pk=serializer.data["id"]))
        answer_serializer = ChoiceSerializer(data=answer)
        if answer_serializer.is_valid():
            answer_serializer.save()   

    
class ChoiceView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()


class LessonView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class ExerciseView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()


class SectionView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = SectionSerializer
    queryset = Section.objects.all()

    def list(self, request):
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        get_no = lambda obj : obj['no']
        for i in range(len(sections)):
            content = ContentSerializer(sections[i].contents.all(), many=True)
            animation = AnimationSerializer(sections[i].animations.all(), many=True)
            image = ImageSerializer(sections[i].images.all(), many=True)
            li = sorted(content.data + animation.data + image.data, key=get_no)
            serializer.data[i]["section"] = li
        return views.Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        section = self.get_object()
        serializer = SectionSerializer(section)
        get_no = lambda obj : obj['no']
        content = ContentSerializer(section.contents.all(), many=True)
        animation = AnimationSerializer(section.animations.all(), many=True)
        image = ImageSerializer(section.images.all(), many=True)
        li = sorted(content.data + animation.data + image.data, key=get_no)
        data = serializer.data
        data["section"] = li
        return views.Response(data, status=status.HTTP_200_OK)


class ContentView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = ContentSerializer
    queryset = Content.objects.all()

    def perform_create(self, serializer):
        sesction = Section.objects.get(pk=self.request.data["section"])
        sesction.content_quantity += 1
        sesction.save()
        if serializer.is_valid():
            serializer.save(no=sesction.content_quantity)


class ImageView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    def perform_create(self, serializer):
        sesction = Section.objects.get(pk=self.request.data["section"])
        sesction.content_quantity += 1
        sesction.save()

        if serializer.is_valid():
            serializer.save(no=sesction.content_quantity)


class AnimationView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = AnimationSerializer
    queryset = Animation.objects.all()

    def perform_create(self, serializer):
        sesction = Section.objects.get(pk=self.request.data["section"])
        sesction.content_quantity += 1
        sesction.save()

        if serializer.is_valid():
            serializer.save(no=sesction.content_quantity)
