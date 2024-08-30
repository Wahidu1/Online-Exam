from django.db import models
from .managers import ExamineeManager
class Examinee(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    education_qualification = models.CharField(max_length=255,blank=True, null=True)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    objects = ExamineeManager() 
    def __str__(self):
        return self.email
    
    
