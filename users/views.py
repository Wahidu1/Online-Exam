from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .forms import ExamineeRegistrationForm, ExamineeLoginForm, ExamineeOTPForm
from .models import Examinee
from contents.email_sender import send_registration_email, send_login_otp_email
from django.core.mail import send_mail
from django.http import BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

import random

def generate_login_otp(length=4):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def register(request):
    if request.session.get('is_logged_in'):
        return redirect("content:dashboard")
    if request.method == 'POST':
        form = ExamineeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            if send_registration_email(name=name, to_email=email):
                form.save()
                # Optionally, you can send OTP here after saving the form.
                messages.success(request, "রেজিস্ট্রেশন সফল হয়েছে")
                # return HttpResponse("Registration Successfully")
                return redirect("user:register")
            else:
                messages.error(request, "একটি সঠিক ইমেল ঠিকানা দিন")

        else:
            messages.error(request, "কোনো কিছুতে সমস্যা হয়েছে")
    else:
        form = ExamineeRegistrationForm()
    context = {
        'form': form, 
        'page_title': 'রেজিস্ট্রেশন',
        'is_logged_in': False}
    return render(request, "users/register.html", context)

def login(request):
    if request.session.get('is_logged_in'):
        return redirect("content:dashboard")
    if request.method == 'POST':
        form = ExamineeLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            examinee = Examinee.objects.filter(email=email).first()
            if examinee:
                otp = generate_login_otp(4)
                examinee_manager = Examinee.objects
                examinee_manager.generate_otp(examinee.email, otp)
                
                if send_login_otp_email(name=examinee.name, to_email=email, otp=otp):
                    
                    messages.success(request, "ওটিপি এর জন্য আপনার ইমেল চেক করুন.")
                    request.session['user_email'] = examinee.email
                    return redirect("user:otp")
                else:
                    messages.error(request, "একটি সঠিক ইমেল ঠিকানা দিন")
                
                # return HttpResponse(f"Examinee: {examinee.name}")
            else:
                messages.error(request, "ইমেল মেলেনি")
            # messages.success(request, "Registration Successfully")
            # return redirect("user:register")
        else:
            messages.error(request, "কোনো কিছুতে সমস্যা হয়েছে")
    else:
        form = ExamineeLoginForm()
    context = {
        'form': form, 
        'is_logged_in': False,
        'page_title' : 'লগইন'
        }
    return render(request, "users/login.html", context)

def otp_verify(request):
    if request.session.get('is_logged_in'):
        return redirect("content:dashboard")
    email = request.session.get('user_email')
    examinee = Examinee.objects.filter(email=email).first()
    if examinee is None:
        messages.error(request, "পরীক্ষার্থী পাওয়া যায় নাই")
        return redirect("user:login")
    if request.method == 'POST':
        form = ExamineeOTPForm(request.POST)
        if form.is_valid():
            digit1 = form.cleaned_data['digit1']
            digit2 = form.cleaned_data['digit2']
            digit3 = form.cleaned_data['digit3']
            digit4 = form.cleaned_data['digit4']
            otp = digit1+digit2+digit3+digit4
            
            examinee_manager = Examinee.objects
            r_messages = examinee_manager.verify_otp(examinee.id, otp)
            if r_messages['verify']:
                request.session['is_logged_in'] = True
                request.session['user_email'] = examinee.email
                return redirect("content:dashboard")
            else:
                messages.error(request, r_messages["messages"])
                return redirect("user:otp")
        else:
            messages.error(request, "কোনো কিছুতে সমস্যা হয়েছে")
    else:
        form = ExamineeOTPForm()
    context = {
        'form': form, 
        'is_logged_in': False,
        'page_title' : "ওটিপি ভেরিফাই"
               
               }
    return render(request, "users/otp-verify.html", context)


