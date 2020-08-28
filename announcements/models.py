from django.db import models
#from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from accounts.models import User
import re
from django.template.loader import get_template
from .tasks import mail_send
from django.conf import settings


# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to='documents/announcements', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super(Announcement, self).save(*args, **kwargs)
        ctx = {
            "title": self.title,
            "description": self.description,
        }
        mail_content = get_template('mail_content.html').render(ctx)
        doc = self.document
        if doc:
            x = 'media/' + str(doc)
            mail_send.delay(mail_content, x)
        else:
            mail_send.delay(mail_content)


    def get_document_url(self):
        if self.document:
            return self.document.name

    def doc_name(self):
        if self.document:
            return re.search('documents/announcements/(.+)',self.document.name).group(1)

    def __str__(self):
        return self.title
