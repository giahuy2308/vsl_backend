from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import Response

from django.http import Http404
from django.db.models import Q

# import requests
from vsl.permissions import IsAuthorOrReadOnly, IsSuperUserOrReadOnly
from .serializers import *
from .models import *

# Create your views here.


class CourseView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            self.queryset = Course.objects.filter(Q(title__icontains=query))
        return super().get_queryset()

    def retrieve(self, request, pk):
        serializer = CourseSerializer(
            self.get_object(), context={"include_topics": True}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopicView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            self.queryset = Topic.objects.filter(Q(title__icontains=query))
        return super().get_queryset()

    def list(self, request):
        serializer = TopicSerializer(
            self.get_queryset(), context={"include_chapters": True}, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        serializer = TopicSerializer(
            self.get_object(), context={"include_chapters": True}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChapterView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            self.queryset = Chapter.objects.filter(Q(title__icontains=query))
        return super().get_queryset()

    def list(self, request):
        serializer = ChapterSerializer(
            self.get_queryset(), context={"include_lessons": True}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        serializer = ChapterSerializer(
            self.get_object(), context={"include_lessons": True}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            self.queryset = Lesson.objects.filter(
                Q(title__icontains=query) | Q(course__title__icontains=query)
            )
        return super().get_queryset()

    def retrieve(self, request, pk):
        serializer = LessonSerializer(
            self.get_object(), context={"include_sections": True}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class SectionView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = SectionSerializer
    queryset = Section.objects.all()

    def retrieve(self, request, pk):
        serializer = SectionSerializer(
            self.get_object(), context={"include_contents": True}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContentView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = ContentSerializer
    queryset = Content.objects.all()


class ImageView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class AnimationView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = AnimationSerializer
    queryset = Animation.objects.all()


class ExerciseView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            self.queryset = Exercise.objects.filter(Q(title__icontains=query))
        return super().get_queryset()


class ExaminationView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            self.queryset = Examination.objects.filter(
                Q(title__icontains=query) | Q(chapter__title__icontains=query)
            )
        return super().get_queryset()

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Examination.objects.get(pk=pk)
        except Examination.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk):
        serializer = ExaminationSerializer(
            self.get_object(), context={"include_questions": True}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def send(self, request, pk):
        assignment = Assignment.objects.create(
            author=request.user, examination=Examination.objects.get(pk=pk), score=0
        )
        score = 0
        for i in range(len(request.data)):
            if not request.data[i]["choice"] == 0:
                userchoice = UserChoice.objects.create(
                    assignment=assignment,
                    question=Question.objects.get(pk=request.data[i]["id"]),
                    choice=Choice.objects.get(pk=request.data[i]["choice"]),
                )
                score += userchoice.question.answer == userchoice.choice.title
        score *= assignment.examination.total_score / len(request.data)
        assignment.score = round(score)
        assignment.save()
        return Response({"status": "Nộp bài thành công"}, status=status.HTTP_200_OK)


class QuestionView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class ChoiceView(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()


class AssignmentView(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            self.queryset = Lesson.objects.filter(
                Q(examination__title__icontains=query) | Q(score__icontains=query)
            )
        return super().get_queryset()

    def retrieve(self, request, pk):
        serializer = AssignmentSerializer(
            self.get_object(), context={"include_questions": True}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserChoiceView(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = UserChoiceSerializer
    queryset = UserChoice.objects.all()


class UserQuestionView(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = UserQuestionSerializer
    queryset = UserQuestion.objects.all()

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            self.queryset = UserQuestion.objects.filter(
                Q(content__icontains=query) | Q(author__icontains=query)
            )
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerForUQView(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = AnswerForUQSerializer
    queryset = AnswerForUQ.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
