from django.db import models
import re
from accounts import models as accounts_model


# Create your models here.
class CourseMaterial(accounts_model.TimeStamp):
    coursematerial_no = models.PositiveIntegerField()
    subject = models.ForeignKey(accounts_model.Subject, related_name='course_materials', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    document = models.FileField(upload_to='documents/course_materials/', null=True, blank=True)

    def get_document_url(self):
        if self.document:
            return self.document.name
    def doc_name(self):
        if self.document:
            return re.search('documents/course_materials/(.+)',self.document.name).group(1)



