import json
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.db.models import Count
from users.models import Examinee
from .models import Exam, Question, Choice, ExamineeResponse, Notification
from django.contrib import messages
from django.http import JsonResponse
from .forms import ExamineeUpdateForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import email_sender

def dashboard(request):
    if not request.session.get('is_logged_in'):
        return redirect("user:login")

    context = {
        'page_name':"dashboard",
        'page_title':"ড্যাশর্বোড",
        'is_logged_in': True,
        }
    return render(request,"contents/dashboard.html", context)

    
def profile_page(request):
    if not request.session.get('is_logged_in'):
        return redirect("user:login")
    context = {
        'page_title':"প্রোফাইল",
        'is_logged_in': True
        }
    return render(request,"contents/profile.html", context)
def exam_cat(request):
    if not request.session.get('is_logged_in'):
        return redirect("user:login")
    exams = Exam.objects.all()
    context =  {
        'exams':exams, 
        'page_name':"exam",
        'page_title':"পরীক্ষা সমূহ",
        'is_logged_in': True
        }
    return render(request,"contents/exam-cat.html",context)
    
def messages_page(request,exam_id):
    if not request.session.get('is_logged_in'):
        return redirect("user:login")
    exam = Exam.objects.filter(id=exam_id).first()
    if exam is None:
        return redirect("content:exam")
    if not exam.is_time_up():
            messages.error(request, "সময় শেষ")
    if not exam.is_start_time():
            messages.warning(request, "পরীক্ষা শুরু হয় নাই")
            
    context = {
        "exam":exam,  
        'is_logged_in': True,
        'page_title' : "বার্তা"
               }
    return render(request, "contents/message.html",context)

def question(request, id):
    if not request.session.get('is_logged_in'):
        return redirect("user:login")
    
    exam = Exam.objects.filter(id=id).first()
    
    if exam.is_time_up() is False:
        return redirect("content:message", exam_id=id)
    if exam.is_start_time()  is False:
        return redirect("content:message", exam_id=id)
    
    
    examinee = Examinee.objects.filter(email=request.session.get('user_email')).first()
    
    examineeResponse = ExamineeResponse.objects.filter(examinee=examinee,question__exam=exam).first()
    # print(examineeResponse)
    
    if examineeResponse:
        messages.success(request, "আপনি ইতি মধ্যে পরীক্ষায় অংশগ্রহণ করছেন")
        return redirect('content:result_submission', exam_id=id)
    
    if request.method == 'POST':
        if exam.is_time_up() is False:
            messages.error(request, f"সময় শেষ হবে: {exam.end_time}")
            return redirect("content:result_submission", exam_id=id)
        # Process the form submission
        for question in Question.objects.filter(exam=exam):
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                selected_choice = get_object_or_404(Choice, id=choice_id)
                ExamineeResponse.objects.create(
                    examinee=examinee,
                    question=question,
                    selected_choice=selected_choice
                )
        messages.success(request, "আপনার পরীক্ষা সাবমিট হয়েছে!")
        return redirect("content:result_submission", exam_id=id)
    
    if exam is not None:
        questions = Question.objects.filter(exam=exam)
        questions_with_choices = []
        
        for question in questions:
            choices = Choice.objects.filter(question=question)
            questions_with_choices.append({
                'question' : question,
                'choices' : choices
            })
        context = {
            'questions_with_choices':questions_with_choices, 
            'examinee':examinee, 
            "exam":exam,
            'page_name':"exam",
            'page_title':"প্রশ্ন",
            'is_logged_in': True

            
            }
        return render(request,"contents/question.html",context)
    else:
        return redirect("content:exam")
    

def results(request, exam_id):
    if not request.session.get('is_logged_in'):
        return redirect("user:login")
    
    examinee = get_object_or_404(Examinee, email=request.session.get('user_email'))
    exam = get_object_or_404(Exam, id=exam_id)
    
    if exam.is_time_up() is True:
        messages.success(request, f"পরীক্ষা শেষ হওয়া পর্যন্ত অপেক্ষা করুন: {exam.end_time}")
        return redirect("content:result_submission", exam_id=exam_id)
    responses = ExamineeResponse.objects.filter(examinee=examinee, question__exam=exam).select_related('question', 'selected_choice')

    correct_count = responses.filter(selected_choice__is_correct=True).count()
    incorrect_count = responses.filter(selected_choice__is_correct=False).count()

    # Prepare a list of response details including the correct answer
    response_details = []
    for response in responses:
        correct_choice = response.question.choices.filter(is_correct=True).first()
        response_details.append({
            'question': response.question.text,
            'your_answer': response.selected_choice.text,
            'is_correct': response.selected_choice.is_correct,
            'correct_answer': correct_choice.text if correct_choice else "No correct answer"
        })

    context = {
        'exam': exam,
        'response_details': response_details,
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'page_title': 'পরীক্ষার ফলাফল',
                    'is_logged_in': True

    }
    return render(request, "contents/result-details.html", context)

def exam_history(request):
    if not request.session.get('is_logged_in'):
        return redirect("user:login")
    
    examinee = Examinee.objects.filter(email=request.session.get('user_email')).first()
    responses = ExamineeResponse.objects.filter(examinee=examinee).select_related('question__exam', 'selected_choice')
    
    # print(responses)
    # Group by exam and calculate the correct/incorrect counts
    exams = {}
    for response in responses:
        exam = response.question.exam
        exam_id = exam.id
        if exam_id not in exams:
            exams[exam_id] = {
                'exam_title': exam.title,
                'total_questions': 0,
                'correct_answers': 0,
                'incorrect_answers': 0
            }
        exams[exam_id]['total_questions'] += 1
        if response.is_correct():
            exams[exam_id]['correct_answers'] += 1
        else:
            exams[exam_id]['incorrect_answers'] += 1
    # import json module

    # return JsonResponse(exams)
    
    context = {
        'page_name':"exam_history",
        'exams':exams,
        'page_title':"পরীক্ষার  ইতিহাস",
                    'is_logged_in': True

        
        
    }
    return render(request, "contents/exam-history.html", context)

def result_submission(request, exam_id):
    if not request.session.get('is_logged_in'):
        return redirect("user:login")
    

    context = {
        'page_name':"exam_history",
        'page_title':"পরীক্ষা জমা",
        'exam_id':exam_id,
        'is_logged_in': True

        
    }
    return render(request, "contents/result-submission.html", context)

def logout(request):
    request.session.flush()
    return redirect('user:login')


def profile_update(request):
    if not request.session.get('is_logged_in'):
        return redirect("user:login")
    examinee = Examinee.objects.filter(email=request.session.get('user_email')).first()
    if request.method == 'POST':
        form = ExamineeUpdateForm(request.POST, request.FILES, instance=examinee)
        if form.is_valid():
            email = form.cleaned_data['email']
            form.save()
            request.session['is_logged_in'] = True
            request.session['user_email'] = email
            messages.success(request, "প্রোফাইল সফল ভাবে আপডেট হয়েছে")
            return redirect("content:profile_update")  # Redirect to a profile page or other relevant page
        else:
            messages.error(request, "কোনো সমস্যা হয়েছে")
    else:
        form = ExamineeUpdateForm(instance=examinee)  # Pre-populate form with existing data

    return render(request, "contents/profile-update.html", {'form': form, 'examinee':examinee,  'is_logged_in': True})


class NotificationListView(ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'contents/notification_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_logged_in'):
            return redirect("user:login")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Fetch examinee based on session email
        self.examinee = Examinee.objects.filter(email=self.request.session.get('user_email')).first()
        return Notification.objects.filter(examinee=self.examinee).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['page_title'] = "নোটিফিকশন"
        context['page_name'] = "notification"
        context['is_logged_in'] = True
        return context


class NotificationDetailView(DetailView):
    
    model = Notification
    context_object_name = 'notification'
    template_name = 'contents/notification-details.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('is_logged_in'):
            return redirect("user:login")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        notification = self.get_object()
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "নোটিফিকশন"
        context['page_name'] = "notification"
        context['is_logged_in'] = True
        return context
