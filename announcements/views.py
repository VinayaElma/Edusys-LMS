from django.shortcuts import render
# Create your views here.
from .models import Announcement
from django.views.generic import ListView,DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewAnnouncementForm
from django.urls import reverse
from django.db.models import Q


def home(request):
    return render(request, 'home.html')


class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'announcement/announcements.html'
    queryset = Announcement.objects.all().order_by('-created_at')
    context_object_name = 'announcements'
    paginate_by = 6



class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    template_name = 'announcement/announcement_new.html'
    form_class = NewAnnouncementForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('announcements:view_announcements')



class SearchResultsView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'announcement/announcements.html'
    paginate_by = 6

    def get_queryset(self): # new
        object_list = Announcement.objects.all()
        query = self.request.GET.get('q')
        if query:
            object_list = object_list.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return object_list