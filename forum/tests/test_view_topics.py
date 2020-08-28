from django.urls import reverse, resolve
from django.test import TestCase
from forum.views import TopicListView
from accounts.models import Subject, Department


class TopicsTests(TestCase):
    def setUp(self):
        dept = Department.objects.create(name='CSE')
        self.subject = Subject.objects.create(code='101', name='Django', department=dept)

    def test_topics_view_success_status_code(self):
        url = reverse('topics', kwargs={'code': self.subject.code})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_topics_view_not_found_status_code(self):
        url = reverse('topics', kwargs={'code': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_topics_url_resolves_topics_view(self):
        view = resolve('/forum/{0}/'.format(self.subject.code))
        self.assertEquals(view.func.view_class, TopicListView)

    def test_topics_view_contains_navigation_links(self):
        topics_url = reverse('topics', kwargs={'code': self.subject.code})
        response = self.client.get(topics_url)
        forum_url = reverse('forum')
        new_topic_url = reverse('new_topic', kwargs={'code': self.subject.code})
        self.assertContains(response, 'href="{0}"'.format(forum_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
