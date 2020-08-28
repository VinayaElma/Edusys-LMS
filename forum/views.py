# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from accounts.models import Subject, User
from django.db.models import Count, Q
from django.utils import timezone
from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from forum.models import Topic, Comment
from .forms import NewTopicForm


class ForumListView(LoginRequiredMixin, ListView):
    model = Subject
    context_object_name = 'subjects'
    template_name = 'forum/forum.html'

    def get_queryset(self):
        user = self.request.user
        return user.subjects.all()


class TopicListView(LoginRequiredMixin, ListView):
    context_object_name = 'topics'
    template_name = 'forum/topics.html'
    paginate_by = 10

    def get_queryset(self):
        self.subject = get_object_or_404(Subject, code=self.kwargs['code'])
        return self.subject.topics.order_by('-modified_date').annotate(replies=Count('comments')-1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
        return context


class NewTopicFormView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = NewTopicForm
    template_name = 'forum/new_topic.html'

    def form_valid(self, form):
        subject = get_object_or_404(Subject, code=self.kwargs['code'])
        user = self.request.user
        topic = form.instance
        topic.created_by = user
        topic.subject = subject
        topic.save()
        comment = Comment.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
        return redirect(self.get_success_url())

    def get_success_url(self):
        code = self.kwargs['code']
        return reverse('forum:topics', kwargs={'code': code})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, code=self.kwargs['code'])
        return context


class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    template_name = 'forum/edit_topic.html'
    form_class = NewTopicForm

    def get_initial(self):
        return {'message': self.object.comments.first().message}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        topic = form.instance
        comment = topic.comments.first()
        comment.message = form.cleaned_data.get('message')
        comment.save()
        topic.save()
        form_class = NewTopicForm
        form_class.base_fields['message'].initial = ""
        return redirect(self.get_success_url())

    def get_success_url(self):
        code = self.kwargs['code']
        pk = self.kwargs['pk']
        return reverse('forum:topic_comments', kwargs={'code': code, 'pk': pk})


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic

    def get_success_url(self):
        code = self.kwargs['code']
        return reverse('forum:topics', kwargs={'code': code})

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class TopicCommentsView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['message']
    template_name = 'forum/topic_comments.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        topic = get_object_or_404(Topic, subject__code=self.kwargs['code'], pk=self.kwargs['pk'])
        user = self.request.user
        comment = form.instance
        comment.created_by = user
        comment.topic = topic
        topic.modified_date = timezone.now()
        comment.save()
        topic.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        code = self.kwargs['code']
        pk = self.kwargs['pk']
        return reverse('forum:topic_comments', kwargs={'code': code, 'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = get_object_or_404(Topic, subject__code=self.kwargs['code'], pk=self.kwargs['pk'])
        first_pk = topic.comments.first().pk
        comment_set = topic.comments.all().exclude(pk=first_pk).order_by('-created_date')
        context['comments'] = list(chain(topic.comments.filter(pk=first_pk), comment_set))
        topic.views += 1
        topic.save(update_fields=["views"])
        context['topic'] = topic
        return context


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'forum/edit_comment.html'
    fields = ('message', )
    pk_url_kwarg = 'comment_pk'
    context_object_name = 'comment'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def get_success_url(self):
        code = self.kwargs['code']
        pk = self.kwargs['pk']
        return reverse('forum:topic_comments', kwargs={'code': code, 'pk': pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_pk'

    def get_success_url(self):
        code = self.kwargs['code']
        pk = self.kwargs['pk']
        return reverse('forum:topic_comments', kwargs={'code': code, 'pk': pk})

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class SearchTopicResultsView(LoginRequiredMixin, ListView):
    context_object_name = 'topics'
    template_name = 'forum/topics.html'
    paginate_by = 10

    def get_queryset(self):
        self.subject = get_object_or_404(Subject, code=self.kwargs['code'])
        queryset = Topic.objects.filter(subject=self.subject)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(description__icontains=query) | Q(comments__message__icontains=query))
        return queryset.order_by('-modified_date').annotate(replies=Count('comments')-1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
        return context
