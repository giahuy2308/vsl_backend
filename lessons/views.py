from rest_framework import viewsets, permissions, views
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


# class ViewMark(generics.RetrieveAPIView):
    


class LessonView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()





class ExerciseView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()


# class MyAnswerView(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = MyAnswerSerializer
#     queryset = MyAnswer.objects.all()

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
class SectionView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = SectionSerializer
    queryset = Section.objects.all()

    def get_content_type(content_type):
        try:
            return ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            raise Http404

    def list(self,request, content_type, obj_pk):
        contenttype = self.get_content_type(content_type)
        section = Section.objects.filter(content_type=contenttype)
        
        

class ContentView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = ContentSerializer
    queryset = Content.objects.all()


class ImageView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class AnimationView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsSuperUserOrReadOnly]
    serializer_class = AnimationSerializer
    queryset = Animation.objects.all()
