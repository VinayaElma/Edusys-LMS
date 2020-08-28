from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Assignment, Question, DescriptiveResult
from accounts.models import Subject
from .forms import NewAssignmentForm, NewFileUploadForm, NewSubmissionForm, NewMarksForm


# Create your views here.
def home(request):
    return render(request, 'base.html')


class SubjectsListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'assignment/assignment_subjects.html'
    context_object_name = 'subjects'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return user.subjects.all()


class SubjectListView(LoginRequiredMixin, ListView):
    template_name = 'assignment/marks_subjects.html'
    context_object_name = 'subjects'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return user.subjects.all()


class SubjectsDetailView(LoginRequiredMixin, ListView):
    template_name = 'assignment/assignments.html'
    context_object_name = 'assignments'
    paginate_by = 10

    def get_queryset(self):
        subject = get_object_or_404(Subject, pk=self.kwargs['pk'])

        assignments = Assignment.objects.filter(subject=subject)
        custom_list = [assignment.id for assignment in assignments if assignment.questions.exists()]
        querset = Assignment.objects.filter(id__in=custom_list)

        return querset.order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk'])
        return context


class MarksListView(LoginRequiredMixin, ListView):
    template_name = 'assignment/marks.html'
    model = DescriptiveResult
    context_object_name = 'answers'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        result_set = DescriptiveResult.objects.none()
        subject = get_object_or_404(Subject, pk=self.kwargs['pk'])

        assignments = Assignment.objects.filter(subject=subject)
        custom_list = [assignment.id for assignment in assignments if assignment.questions.exists()]
        assignments = Assignment.objects.filter(id__in=custom_list)

        if user.user_type == 'student':

            for assignment in assignments:
                if assignment.overdue_status():
                    questions = assignment.questions.all()
                    question = questions[0]
                    answers = question.descriptive_answers.all()
                    user_answer = answers.filter(student=user)
                    if not user_answer:
                        answer = DescriptiveResult.objects.create(student=user, question=question, marks=0)
                        answer.save()

            for assignment in assignments:
                questions = assignment.questions.all()
                question = questions[0]
                answers = question.descriptive_answers.all()
                user_answer = answers.filter(student=user)
                result_set |= user_answer

        else:

            result_set |= assignments

        return result_set.order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk'])
        return context


class StudentsListView(LoginRequiredMixin, ListView):
    template_name = 'assignment/students_marks.html'
    model = DescriptiveResult
    context_object_name = 'answers'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        subject = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        questions = assignment.questions.all()
        question = questions[0]
        users = subject.users.all()

        for user in users:
            if user.user_type == 'student':
                if assignment.overdue_status():
                    answers = question.descriptive_answers.all()
                    user_answer = answers.filter(student=user)
                    if not user_answer:
                        answer = DescriptiveResult.objects.create(student=user, question=question, marks=0)
                        answer.save()

        answers = question.descriptive_answers.all()
        return answers.order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = 0
        count = 0
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        context['assignment'] = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        questions = context['assignment'].questions.all()
        context['question'] = questions[0]
        answers = context['question'].descriptive_answers.all()
        users = context['subject'].users.all()
        for user in users:
            if user.user_type == 'student':
                count = count + 1
        for answer in answers:
            if answer.marks is not None:
                total = total + answer.marks
        try:
            context['average'] = total / count
        except ZeroDivisionError:
            context['average'] = 0
        return context


class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Assignment
    template_name = 'assignment/assignment_form.html'
    form_class = NewAssignmentForm

    def form_valid(self, form):
        subject = get_object_or_404(Subject, pk=self.kwargs['pk'])
        form.instance.subject = subject
        form.instance.assignment_type = 'File Upload'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        pk_alt = self.kwargs['pk']
        pk = self.object.id
        # return "/subjects/" + str(pk)

        return reverse('assignments:question_file_upload', kwargs={
            'pk_alt': pk_alt,
            'pk': pk,
        })


class AssignmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Assignment
    form_class = NewAssignmentForm
    template_name = 'assignment/assignment_update.html'

    def form_valid(self, form):
        subject = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        form.instance.subject = subject
        form.instance.assignment_type = 'File Upload'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        return context

    def get_success_url(self):
        pk_alt = self.kwargs['pk_alt']
        pk_al = self.kwargs['pk']
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        questions = assignment.questions.all()
        # return "/subjects/" + str(pk)
        return reverse('assignments:question_file_update', kwargs={
            'pk_alt': pk_alt,
            'pk_al': pk_al,
            'pk': questions[0].pk,
        })


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'assignment/assignment_detail.html'

    def get_object(self):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        return assignment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        context['assignment'] = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        questions = context['assignment'].questions.all()
        context['question'] = questions[0]
        answers = DescriptiveResult.objects.filter(student=self.request.user, question=questions[0])
        try:
            context['answer'] = answers[0]
        except IndexError:
            context['answer'] = None

        return context


class AssignmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Assignment
    form_class = NewAssignmentForm
    template_name = 'assignment/assignment_confirm_delete.html'

    def form_valid(self, form):
        subject = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        form.instance.subject = subject
        return super().form_valid(form)

    def get_success_url(self):
        pk_alt = self.kwargs['pk_alt']
        return reverse('assignments:view_assignments', kwargs={
            'pk': pk_alt,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        context['assignment'] = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        questions = self.object.questions.all()
        for question in questions:
            question.document.delete()
        return super().delete(self, request, *args, **kwargs)


class FileUploadCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'assignment/file_upload_form.html'
    form_class = NewFileUploadForm

    def form_valid(self, form):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        form.instance.assignment = assignment
        assignment.marks = form.instance.marks
        assignment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        context['assignment'] = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        pk_alt = self.kwargs['pk_alt']
        return reverse('assignments:view_assignments', kwargs={
            'pk': pk_alt,
        })


class FileUploadUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = NewFileUploadForm
    template_name = 'assignment/file_upload_update.html'

    def form_valid(self, form):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk_al'])
        form.instance.assignment = assignment
        assignment.marks = form.instance.marks
        assignment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        context['assignment'] = get_object_or_404(Assignment, pk=self.kwargs['pk_al'])
        return context

    def get_success_url(self):
        pk_alt = self.kwargs['pk_alt']
        return reverse('assignments:view_assignments', kwargs={
            'pk': pk_alt,
        })


class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = DescriptiveResult
    template_name = 'assignment/submission_form.html'
    form_class = NewSubmissionForm

    def form_valid(self, form):
        form.instance.student = self.request.user
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        form.instance.question = question
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        context['assignment'] = get_object_or_404(Assignment, pk=self.kwargs['pk_al'])
        context['question'] = get_object_or_404(Question, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        pk_alt = self.kwargs['pk_alt']
        pk = self.kwargs['pk_al']
        # return "/subjects/" + str(pk)

        return reverse('assignments:detail_assignments', kwargs={
            'pk_alt': pk_alt,
            'pk': pk,
        })


class SubmissionUpdateView(LoginRequiredMixin, UpdateView):
    model = DescriptiveResult
    template_name = 'assignment/submission_form.html'
    form_class = NewSubmissionForm

    def form_valid(self, form):
        form.instance.student = self.request.user
        question = get_object_or_404(Question, pk=self.kwargs['pk_a'])
        form.instance.question = question
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        context['assignment'] = get_object_or_404(Assignment, pk=self.kwargs['pk_al'])
        context['question'] = get_object_or_404(Question, pk=self.kwargs['pk_a'])
        return context

    def get_success_url(self):
        pk_alt = self.kwargs['pk_alt']
        pk = self.kwargs['pk_al']

        return reverse('assignments:detail_assignments', kwargs={
            'pk_alt': pk_alt,
            'pk': pk,
        })


class AnswerListView(LoginRequiredMixin, ListView):
    model = DescriptiveResult
    template_name = 'assignment/answers.html'
    context_object_name = 'answers'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        context['assignment'] = get_object_or_404(Assignment, pk=self.kwargs['pk_al'])
        context['question'] = get_object_or_404(Question, pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        answers = question.descriptive_answers.all()
        answers = answers.exclude(document='')
        return answers.order_by('-created_date')


class MarkUploadView(LoginRequiredMixin, UpdateView):
    template_name = 'assignment/answer_detail.html'
    model = DescriptiveResult
    form_class = NewMarksForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        context['assignment'] = get_object_or_404(Assignment, pk=self.kwargs['pk_al'])
        context['question'] = get_object_or_404(Question, pk=self.kwargs['pk_a'])
        context['answer'] = get_object_or_404(DescriptiveResult, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        pk_alt = self.kwargs['pk_alt']
        pk_al = self.kwargs['pk_al']
        pk = self.kwargs['pk_a']

        return reverse('assignments:view_answers', kwargs={
            'pk_alt': pk_alt,
            'pk_al': pk_al,
            'pk': pk,
        })
