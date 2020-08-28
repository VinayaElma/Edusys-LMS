from django.urls import reverse, resolve
from django.test import TestCase
from forum.views import NewTopicFormView
from accounts.models import Subject, Department, User
from forum.models import Topic, Comment
from forum.forms import NewTopicForm


class NewTopicsTests(TestCase):
    def setUp(self):
        dept = Department.objects.create(name='CSE')
        self.subject = Subject.objects.create(code='101', name='Django', department=dept)
        User.objects.create_user(username='john', email='john@doe.com', password='123')

    def test_new_topics_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'code': self.subject.code})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_topics_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'code': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_topics_url_resolves_topics_view(self):
        view = resolve('/forum/{0}/new/'.format(self.subject.code))
        self.assertEquals(view.func.view_class, NewTopicFormView)

    def test_topics_view_contains_navigation_links(self):
        new_topic_url = reverse('new_topic', kwargs={'code': self.subject.code})
        response = self.client.get(new_topic_url)
        topics_url = reverse('topics', kwargs={'code': self.subject.code})
        self.assertContains(response, 'href="{0}"'.format(topics_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'code': self.subject.code})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'code': self.subject.code})
        data = {
            'description': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Comment.objects.exists())

    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'code': self.subject.code})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('new_topic', kwargs={'code': self.subject.code})
        data = {
            'description': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Comment.objects.exists())

    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'code': self.subject.code})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)
