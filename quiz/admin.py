from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Quiz)
admin.site.register(Quiz_Question)
admin.site.register(Choice)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)
admin.site.register(StudentAttemptedList)


