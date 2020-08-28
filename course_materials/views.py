from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import CourseMaterial
from accounts.models import Subject, User, Department
from .forms import NewCourseMaterialForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request, 'base.html')


class SubjectsListView(LoginRequiredMixin, ListView):
    model = CourseMaterial
    template_name = 'course_material/course_subjects.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        user = self.request.user
        return user.subjects.all()



class SubjectsDetailView(LoginRequiredMixin, DetailView):
    template_name = 'course_material/course_materials.html'
    context_object_name = 'subject'
    paginate_by = 10

    def get_object(self):
        subject = get_object_or_404(Subject, pk=self.kwargs['pk'])
        return subject



class SubjectsDetailView1(LoginRequiredMixin, DetailView):
    template_name = 'course_material/course_teacher.html'
    context_object_name = 'subject'
    paginate_by = 10

    def get_object(self):
        subject = get_object_or_404(Subject, pk=self.kwargs['pk'])
        return subject


class CourseMaterialCreateView(LoginRequiredMixin,CreateView):
    model = CourseMaterial
    template_name = 'course_material/course_material_form.html'
    form_class = NewCourseMaterialForm

    def form_valid(self, form):
        subject = get_object_or_404(Subject, pk=self.kwargs['pk'])
        form.instance.subject = subject
        subject.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        pk_alt = self.kwargs['pk']
        pk = self.object.id

        return reverse('course_materials:view_teacher_courses', kwargs={
            'pk': pk_alt,
        })

class CourseMaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = CourseMaterial
    form_class = NewCourseMaterialForm
    template_name = 'course_material/coursemat_confirm_delete.html'

    def form_valid(self, form):
        subject = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        form.instance.subject = subject
        return super().form_valid(form)

    def get_success_url(self):
        pk_alt = self.kwargs['pk_alt']
        return reverse('course_materials:view_teacher_courses', kwargs={
            'pk': pk_alt,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        context['course_material'] = get_object_or_404(CourseMaterial, pk=self.kwargs['pk'])
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(self, request, *args, **kwargs)


class CourseMaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = CourseMaterial
    form_class = NewCourseMaterialForm
    template_name = 'course_material/course_material_update.html'

    def form_valid(self, form):
        subject = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        form.instance.subject = subject
        subject.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk_alt'])
        return context

    def get_success_url(self):
        pk_alt = self.kwargs['pk_alt']
        pk_al = self.kwargs['pk']
        return reverse('course_materials:view_teacher_courses', kwargs={
            'pk': pk_alt,
        })


class SearchResultsView(LoginRequiredMixin, ListView):
    model = CourseMaterial
    template_name = 'course_material/course_materials.html'

    def get_queryset(self): # new
        self.subject = get_object_or_404(Subject, pk=self.kwargs['pk'])
        object_list = CourseMaterial.objects.filter(subject=self.subject) #
        query = self.request.GET.get('q')
        if query:
            object_list = object_list.filter(
            Q(coursematerial_no__icontains=query) | Q(description__icontains=query)
        )
        print(1)
        print(object_list)
        print(query)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
        context['search_result'] = self.request.GET.get('q')
        return context



class SearchResultsViews(LoginRequiredMixin, ListView):
    model = CourseMaterial
    template_name = 'course_material/course_teacher.html'

    def get_queryset(self): # new
        self.subject = get_object_or_404(Subject, pk=self.kwargs['pk'])
        object_list = CourseMaterial.objects.filter(subject=self.subject) #
        query = self.request.GET.get('q')
        if query:
            object_list = object_list.filter(
            Q(coursematerial_no__icontains=query) | Q(description__icontains=query)
        )
        print(1)
        print(object_list)
        print(query)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
        context['search_result'] = self.request.GET.get('q')
        return context
