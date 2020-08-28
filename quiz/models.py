from django.db import models
from accounts.models import Subject
from accounts.models import User


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    date = models.DateField(null=True)
        
    def __str__(self):

        return self.name


class Quiz_Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField(null=True, max_length=100)

    def __str__(self):
        return self.question 


class Choice(models.Model):
    question = models.ForeignKey(Quiz_Question, on_delete=models.CASCADE, related_name='answers')
    choice = models.CharField(null=True, max_length=55)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice


class StudentAttemptedList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Subject, related_name='interested_students')
    
  

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('question')
        return questions

    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    student = models.ForeignKey(StudentAttemptedList, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)     


class StudentAnswer(models.Model):
    student = models.ForeignKey(StudentAttemptedList, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='+')
