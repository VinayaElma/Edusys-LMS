import os
import re
import uuid
from django.db import models
from django.utils import timezone

from accounts import models as accounts_model


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/logos', filename)


# Create your models here.
ASSIGNMENT_TYPES = [
    ('Quiz', 'Quiz'),
    ('File_upload', 'File Upload'),
]


class Assignment(accounts_model.TimeStamp):
    assignment_no = models.PositiveIntegerField()
    subject = models.ForeignKey(accounts_model.Subject, related_name='assignments', on_delete=models.CASCADE)
    marks = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    description = models.CharField(max_length=255, null=True, blank=True)
    assignment_type = models.CharField(max_length=11, choices=ASSIGNMENT_TYPES)
    due_date = models.DateTimeField(null=True, blank=True)

    def overdue_status(self):
        if self.due_date and timezone.now() > self.due_date:
            return True
        else:
            return False


class Question(accounts_model.TimeStamp):
    question = models.CharField(max_length=255)
    assignment = models.ForeignKey(Assignment, related_name='questions', on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/questions/', null=True, blank=True)
    marks = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)


class DescriptiveResult(accounts_model.TimeStamp):
    student = models.ForeignKey(accounts_model.User, related_name='submission', on_delete=models.CASCADE)
    marks = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=4)
    document = models.FileField(upload_to='documents/answers/', null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    question = models.ForeignKey(Question, related_name='descriptive_answers', on_delete=models.CASCADE)

    def doc_name(self):
        if self.document:
            return re.search('documents/answers/(.+)', self.document.name).group(1)
