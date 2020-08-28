from django.urls import reverse, resolve
from django.test import TestCase
from forum.views import TopicCommentsView
from accounts.models import Subject, Department, User
from forum.models import Topic, Comment


class TopicComments(TestCase):
    def setUp(self):
        dept = Department.objects.create(name='CSE')
        self.subject = Subject.objects.create(code='101', name='Django', department=dept)
        user = User.objects.create(username='james', email='james@bond.com', password='123')
        self.topic = Topic.objects.create(description="abcdgefgh", subject=self.subject, created_by=user)
        Comment.objects.create(message='Dulce et decorem est', topic=self.topic, created_by=user)
        url = reverse('topic_comments', kwargs={'pk': self.topic.pk, 'code': self.subject.code})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/forum/{0}/topics/{1}/'.format(self.subject.code, self.topic.pk))
        self.assertEquals(view.func.view_class, TopicCommentsView)
