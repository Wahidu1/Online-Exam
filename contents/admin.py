from django.contrib import admin
from .models import Exam, Question, Choice, ExamineeResponse, Notification
# Register your models here.
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(ExamineeResponse)
admin.site.register(Notification)

