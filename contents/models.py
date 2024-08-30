from django.db import models
from users.models import Examinee
from django.utils import timezone


class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def is_time_up(self):
        if self.end_time > timezone.now():
            return True
        else:
            return False
        
    def is_start_time(self):
        if self.start_time < timezone.now():
            return True
        else:
            return False

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class ExamineeResponse(models.Model):
    examinee = models.ForeignKey(Examinee, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='responses', on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, related_name='responses', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.examinee} - {self.question.text} - {self.selected_choice.text}'
    
    def is_correct(self):
        return self.selected_choice.is_correct
    
    
class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    examinee = models.ForeignKey(Examinee, on_delete=models.CASCADE, null=True, blank=True)
    
