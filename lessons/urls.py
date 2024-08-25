from rest_framework import routers
from django.urls import path
from .views import *

router = routers.SimpleRouter()
router.register(r'courses', CourseView)
router.register(r'course/userquestion', UserQuestionView)
router.register(r'course/answerforuq', AnswerForUQView)
router.register(r'course/lesson', LessonView)
router.register(r'course/examination', ExaminationView)
router.register(r'course/question', QuestionView)
router.register(r'course/choice', ChoiceView)
router.register(r'course/assignment', AssignmentView)
router.register(r'course/userchoice', UserChoiceView)
router.register(r'course/section', SectionView)
router.register(r'course/exercise', ExerciseView)
# router.register(r'myanswer', MyAnswerView)
router.register(r'course/content', ContentView)
router.register(r'course/image', ImageView)
router.register(r'course/animation', AnimationView)


urlpatterns = router.urls