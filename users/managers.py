from django.db import models
from django.utils import timezone


class ExamineeManager(models.Manager):
    def create_user(self, name, email, father_name, education_qualification, phone, image=None, **extra_fields):
        examinee = self.create(
            name=name,
            email=email,
            father_name=father_name,
            education_qualification=education_qualification,
            phone=phone,
            image=image,)
        return examinee
    
    def verify_otp(self, id, otp):
        examinee = self.get(id=id)
        if examinee:
            message = {
                    "verify": False,
                    "messages": "",
                    }
            if examinee.otp_expiry < timezone.now():
                message['verify'] = False
                message["messages"] = "ওটিপি এর সময় শেষ"
                return message
            elif examinee.otp != otp:
                message['verify'] = False
                message["messages"] = "ওটিপি মিলে নাই"
                return message
            elif examinee.otp == otp and examinee.otp_expiry > timezone.now():
                examinee.otp_verified = True
                examinee.save()
                message['verify'] = True
                message["messages"] = "Login Successfully"
                return message
            else:
                message['verify'] = False
                message["messages"] = "Some Thing is wrong"
                return message
        else:
            message['verify'] = False
            message["messages"] = "Member Not Found"
            return message
    
    def generate_otp(self, email, otp):
        examinee = self.get(email=email)
        expiry_time = timezone.now() + timezone.timedelta(minutes=5)
        examinee.otp = otp
        examinee.otp_expiry = expiry_time
        examinee.otp_verified = False
        examinee.save()
        return examinee