from django.urls import path
from quiz import views as quiz_views

app_name='quiz'

urlpatterns = [
   
    path('', quiz_views.Baseview.as_view(), name='quiz_home'),
    path('quizsearch/', quiz_views.QuizSearchResult.as_view(), name='quiz_search'),
    path('delete/<int:pk>/', quiz_views.QuizDeleteView.as_view(), name='quiz_delete'),   
    path('newquiz/', quiz_views.NewQuiz.as_view(), name='newquiz'),
    path('newquiz/<int:pk>/newquestion/', quiz_views.QuestionAdd, name='question_add'),        
    path('taken/', quiz_views.TakenQuizListView.as_view(), name='taken_quiz_list'),
    path('questionlist/<int:pk>/', quiz_views.QuestionListView.as_view(), name='question_list'),
    path('questionlist/<int:pk>/question/<int:ques_pk>/delete', quiz_views.QuestionDeleteView.as_view(), name='question_delete'),
    path('<int:pk>/', quiz_views.Quizconf.as_view(), name='quizconf'),   
    path('<int:pk>/quizresult', quiz_views.Quizresultview.as_view(), name='quiz_result'),
    path('<int:pk>/takequizz', quiz_views.TakeQuiz, name='takequiz'),
    path('<int:pk>/takequizz/takenquizview', quiz_views.AfterQuizList.as_view(), name='after_quiz'),       
]
