from django.contrib import admin
from .models import Assignment, Question, DescriptiveResult

# Register your models here.
admin.site.register(Assignment)
admin.site.register(Question)
admin.site.register(DescriptiveResult)
