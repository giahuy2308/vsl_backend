from rest_framework import routers
from django.urls import path
from .views import *

router = routers.SimpleRouter()
router.register(r'userquestion', UserQuestionView)
router.register(r'answerforuq', AnswerForUQView)
router.register(r'lesson', LessonView)
router.register(r'examination', ExaminationView)
router.register(r'question', QuestionView)
router.register(r'choice', ChoiceView)
router.register(r'section', SectionView)
router.register(r'exercise', ExerciseView)
# router.register(r'myanswer', MyAnswerView)
router.register(r'content', ContentView)
router.register(r'image', ImageView)
router.register(r'animation', AnimationView)


urlpatterns = [
    path("section/<str:content_type>/<int:obj_pk>/", SectionView.as_view({
        'get':'list'
    }))
] + router.urls