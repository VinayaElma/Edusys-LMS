from django.db import models
import os
from accounts.models import TimeStamp, User, Subject
from forum.validators import validate_file_extension
from django.utils.text import Truncator


class Topic(TimeStamp):
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    subject = models.ForeignKey(Subject, related_name='topics', on_delete=models.CASCADE)
    document = models.FileField(upload_to='topics/documents/', validators=[validate_file_extension], null=True, blank=True)

    def __str__(self):
        return self.description

    def get_truncated_description(self):
      return self.description[:30]

    def is_document_image(self):
        ext_list = [".jpg", ".jpeg", ".png", ".gif", ".svg"]
        doc_name, doc_extension = os.path.splitext(self.document.name)
        for ext in ext_list:
            if ext == doc_extension:
                return True


class Comment(TimeStamp):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.message[:30]
