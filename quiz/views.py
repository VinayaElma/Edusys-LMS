from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Quiz, Quiz_Question, Choice, StudentAnswer, TakenQuiz, StudentAttemptedList
from django.views.generic import ListView, CreateView, DeleteView
from django.db.models import Count, Sum
from django.utils import timezone
import datetime
from .forms import AddQuizForm, QuestionModelForm, TakeQuizForm, ChoiceFormset


class Baseview(LoginRequiredMixin, ListView):
    model = Quiz
    context_object_name = 'quizes'
    template_name = 'quiz/quiz_stud.html'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        sub = user.subjects.all()
        queryset = Quiz.objects.filter(subject__in=sub)
        return queryset


class Quizconf(LoginRequiredMixin, ListView):
    model = Quiz
    context_object_name = 'quizes'
    template_name = 'quiz/quiz_conf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        query = get_object_or_404(Quiz, pk=self.kwargs.get('pk'))
        context['qcount'] = Quiz_Question.objects.filter(quiz=query).count()        
        
        try:
            query = get_object_or_404(StudentAttemptedList, user=user)
            if query.quizzes.filter(pk=self.kwargs.get('pk')).exists():
                context['check'] = 0
            else:
                context['check'] = 1
        except:
            context['check'] = 1
            
        return context
    
    def get_queryset(self):
        queryset = get_object_or_404(Quiz, pk=self.kwargs.get('pk'))
        return queryset


class NewQuiz(LoginRequiredMixin, CreateView):
    model = Quiz
    form_class = AddQuizForm   
    template_name = 'quiz/new_quiz.html'

    def render_to_response(self, context):
        user = self.request.user
        if user.user_type == 'student':
            return redirect('quiz:quiz_home')
        return super(NewQuiz, self).render_to_response(context)    

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        return redirect('quiz:question_add', pk=quiz.pk)

    def get_form_kwargs(self):
        kwargs = super(NewQuiz,self).get_form_kwargs() 
        kwargs['user'] = self.request.user
        return kwargs


class TakenQuizListView(LoginRequiredMixin, ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'    
    template_name = 'quiz/taken_quiz.html'
    paginate_by = 5

    def render_to_response(self, context):
        user=self.request.user
        if user.user_type == 'teacher':
            return redirect('quiz:quiz_home')
        return super(TakenQuizListView, self).render_to_response(context)   

    def get_queryset(self):
        user = self.request.user
        queryset = TakenQuiz.objects.filter(student__user=user)\
            .annotate(qcount=Count('quiz__questions'))\
            .order_by('quiz__name')       
        return queryset
        

class Quizresultview(LoginRequiredMixin, ListView):
    model = TakenQuiz
    context_object_name = "taken_quizs"
    template_name = "quiz/quiz_result.html"
    
    def render_to_response(self, context):
        user = self.request.user
        if user.user_type == 'student':
            return redirect('quiz:quiz_home')
        return super(Quizresultview, self).render_to_response(context)   

    def queryset(self):
        query = get_object_or_404(Quiz, pk=self.kwargs.get('pk'))
        queryset = TakenQuiz.objects.filter(quiz=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ques = get_object_or_404(Quiz, pk=self.kwargs.get('pk'))
        context['qcount'] = Quiz_Question.objects.filter(quiz=ques).count()
        return context


class QuizDeleteView(LoginRequiredMixin, DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'quiz/quiz_delete_confirm.html'
    success_url = reverse_lazy('quiz:quiz_home')

    def render_to_response(self, context):
        user = self.request.user
        quiz = get_object_or_404(Quiz, pk=self.kwargs.get('pk'))
        if quiz.owner != user:
            return redirect('quiz:quiz_home')            
        return super(QuizDeleteView, self).render_to_response(context) 

    def delete(self, request, *args, **kwargs):                
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Quiz.objects.filter(pk=self.kwargs.get('pk'))
        return queryset


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Quiz_Question
    context_object_name = "quest"
    template_name = "quiz/question_delete_confirm.html"    
    pk_url_kwarg = 'ques_pk'

    def render_to_response(self, context):
        user = self.request.user
        quiz = get_object_or_404(Quiz, pk=self.kwargs.get('pk'))
        if quiz.owner != user:
            return redirect('quiz:quiz_home')   

        return super(QuestionDeleteView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):                
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Quiz_Question.objects.filter(pk=self.kwargs.get('ques_pk'))
        return queryset  

    def get_success_url(self):
        question = self.get_object()
        return reverse('quiz:question_list', kwargs={'pk': question.quiz_id})    
    
    
class QuestionListView(LoginRequiredMixin, ListView):
    model = Quiz_Question
    template_name = "quiz/question_list.html"
    context_object_name = "questions"
    paginate_by = 8

    def get_queryset(self):
        quiz = get_object_or_404(Quiz, pk=self.kwargs.get('pk'))
        queryset = Quiz_Question.objects.filter(quiz=quiz)         
        return queryset   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = get_object_or_404(Quiz, pk=self.kwargs.get('pk'))
        context['quiz'] = quiz
        context['choices'] = Choice.objects.filter(question__quiz=quiz)
        context['now'] = timezone.now().date()
        return context


class AfterQuizList(LoginRequiredMixin, ListView):
    model = Quiz_Question
    template_name = "quiz/after_quiz.html"
    context_object_name = "questions"
       
    def get_queryset(self):
        quiz = get_object_or_404(Quiz, pk=self.kwargs.get('pk'))
        queryset = Quiz_Question.objects.filter(quiz=quiz) 
        return queryset   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = get_object_or_404(Quiz, pk=self.kwargs.get('pk'))
        context['quiz'] = quiz
        context['choices'] = Choice.objects.filter(question__quiz=quiz)
        context['answers'] = StudentAnswer.objects.filter(answer__question__quiz=quiz)
        user = self.request.user
        queryset = get_object_or_404(TakenQuiz, quiz=quiz, student__user=user)
        context['scores'] = queryset        
        context['qcount'] = Quiz_Question.objects.filter(quiz=quiz).count()
        return context


class QuizSearchResult(LoginRequiredMixin, ListView):
    model = Quiz
    context_object_name = 'quizes'
    template_name = 'quiz/quiz_stud.html'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        sub = user.subjects.all()
        queryset = Quiz.objects.filter(subject__in=sub)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

@login_required
def QuestionAdd(request, pk):
    user = request.user
    if user.user_type == 'student':
        return redirect('quiz:quiz_home')
    template_name = 'quiz/newques.html'
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'GET':
        questionform = QuestionModelForm(request.GET or None)
        formset = ChoiceFormset(queryset=Choice.objects.none())
    elif request.method == 'POST':
        questionform = QuestionModelForm(request.POST)
        formset = ChoiceFormset(request.POST)
        if questionform.is_valid() and formset.is_valid():
            
            question = questionform.save(commit=False)
            question.quiz = quiz
            question.save()
            
            for form in formset:
                
                choice = form.save(commit=False)
                choice.question = question                                
                choice.save()
            return redirect('quiz:question_add', quiz.pk)
    return render(request, template_name, {
        'questionform': questionform,
        'quiz': quiz,
        'formset': formset,
    })

@login_required
def TakeQuiz(request, pk):
    
    user = request.user
    if user.user_type == 'teacher':
        return redirect('quiz:quiz_home')
    try:
        StudentAttemptedList.objects.create(user=user)
    except:  
        query = get_object_or_404(StudentAttemptedList, user=user)
    query = get_object_or_404(StudentAttemptedList, user=user)
    
    if query.quizzes.filter(pk=pk).exists():
        
        return redirect('quiz:taken_quiz_list')

    quiz = get_object_or_404(Quiz, pk=pk)
    
    if (quiz.date != timezone.now().date()):
        messages.warning(request, "Attempt on the date")
        return render(request, 'quiz/quiz_error.html')
    
    total_questions = quiz.questions.count()
    unanswered_questions = query.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            
            student_answer = form.save(commit=False)
            student_answer.student = query
            student_answer.save()

            if query.get_unanswered_questions(quiz).exists():
                return redirect('quiz:takequiz', pk)
            else:
                correct_answers = query.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()                
                TakenQuiz.objects.create(student=query, quiz=quiz, score=correct_answers)
                user.score = TakenQuiz.objects.filter(student=query).aggregate(Sum('score'))['score__sum']
                user.save()                                
                return redirect('quiz:after_quiz', pk)                            
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'quiz/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,        
        'answered_questions': total_questions - total_unanswered_questions,
        'total_questions': total_questions
    })
            