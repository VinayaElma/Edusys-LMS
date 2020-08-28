from django.urls import reverse, resolve
from django.test import TestCase

from forum.views import ForumListView
from accounts.models import Subject, Department


class ForumTests(TestCase):
    def setUp(self):
        dept = Department.objects.create(name='CSE')
        self.subject = Subject.objects.create(code='101', name='Django', department=dept)
        url = reverse('forum')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/forum/')
        self.assertEquals(view.func.view_class, ForumListView)

    def test_home_view_contains_link_to_topics_page(self):
        topics_url = reverse('topics', kwargs={'code': self.subject.code})
        self.assertContains(self.response, 'href="{0}"'.format(topics_url))
