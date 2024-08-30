from django.core.mail import send_mail
from django.http import BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

def send_registration_email(name, to_email):
    subject = 'Welcome to Online – Account Registration Successful!'
    html_message = render_to_string('users/email-registration.html', {
        'first_name': name,
        'company_name': 'Online Exam',
        'support_email': 'support@gmail.com',
        'current_year': timezone.now().year,
    })
    plain_message = strip_tags(html_message)
    from_email = 'wahidulislamofficialbd@gmail.com'
    to = to_email
    try:
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        return True
    except BadHeaderError:
        return False
        

def send_login_otp_email(name,to_email, otp):
    subject = 'Your OTP Code for Login'
    html_message = render_to_string('users/email-otp.html', {
        'first_name': name,
        'otp': otp,
        'otp_expiry_minutes': 5,  # Adjust the expiry time as needed
        'company_name': 'Online Exam',
        'current_year': timezone.now().year,
    })
    plain_message = strip_tags(html_message)
    from_email = 'wahidulislamofficialbd@gmail.com'
    to = to_email
    try:
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        return True
    except BadHeaderError:
        return False
    
