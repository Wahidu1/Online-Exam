from django import forms
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from .forms import ExamForm, ExamineeUpdateForm, MCQAddForm
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from contents.models import Exam, Choice, Notification, Question, ExamineeResponse
from users.models import Examinee
from django.views.generic import View
from django.db.models import Count

class LoginPageView(View):
    template_name = 'backend/login.html'
    
    def get(self, request):
        message = ''
        return render(request, self.template_name, context={'message': message})
        
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        if username  and password:
            user = authenticate(
            username=username,
            password=password,
            )
            if user is not None:
                login(request, user)
                return redirect('backend:dashboard')
        
        return render(request, self.template_name, context={})

@login_required(login_url="login/")
def logout_page(request):
    logout(request)
    return redirect("backend:login")
    
@login_required(login_url="login/")
def dashboard(request):
    number_of_exam = Exam.objects.count()
    number_of_examinee = Examinee.objects.count()
    
    context = {
        'page_name': 'dashboard',
        'page_title': "Dashboard",
        'number_of_examinee':number_of_examinee,
        'number_of_exam' : number_of_exam
    }
    return render(request, "backend/dashboard.html", context)

@login_required(login_url="login/")
def exam_add(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request ,"Exam Add Successfully")
            return redirect("backend:exam_add")
        else:
            messages.error(request ,"Error!! Exam Not Add")
    
    form = ExamForm()
    context = {
        'page_name': 'exam_add',
        'page_title': "Exam Add",
        'form':form
    }
    return render(request, "backend/exam-add.html", context)

@login_required(login_url="login/")
def exam_list(request):
    exams = Exam.objects.all()
    context = {
        'page_name': 'exam_list',
        'page_title': "Exam List",
        'exams' : exams
    }
    return render(request, "backend/exam-list.html", context)

@login_required(login_url="login/")
def exam_edit(request, exam_id):
    exam = Exam.objects.filter(id=exam_id).first()
    if exam is None:
        messages.error("Exam Not Found")
        return redirect("backend:exam_list")
    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)
        
        if form.is_valid():
            form.save()
            messages.success(request ,"Exam Update Successfully")
            return redirect("backend:exam_edit", exam_id=exam_id)
        else:
            messages.error(request ,"Error!! Exam Not Add")
    
    form = ExamForm(instance=exam)
    context = {
        'page_name': 'exam_edit',
        'page_title': "Exam Edit",
        'form':form
    }
    return render(request, "backend/exam-edit.html", context)

@method_decorator(login_required(login_url="login/"), name='dispatch')
class QuestionAddView(View):
    template_name = 'backend/question-add.html'
    context = {
        }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = "question_add"
        context["page_title"] = "Question Add"
        return context
    def get(self, request, *args, **kwargs):
        exam_id = request.GET.get('exam_id')
        num_questions = int(request.GET.get('number_of_question', 10))
        exams = Exam.objects.all()

        if not exam_id:
            return render(request, self.template_name, {'exams': exams, 'error': 'No exam ID provided.'})

        exam = get_object_or_404(Exam, id=exam_id)

        MCQAddFormSet = formset_factory(MCQAddForm, extra=0)
        initial_data = [{'exam': exam} for _ in range(num_questions)]
        formset = MCQAddFormSet(initial=initial_data)

        self.context['exam']=exam
        self.context['exams']=exams
        self.context['formset']=formset
        self.context['num_questions']=num_questions
        
        
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        exams = Exam.objects.all()
        MCQAddFormSet = formset_factory(MCQAddForm, extra=0)
        formset = MCQAddFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                form.save()
                messages.success(request, "Question Add Successfully")
            return redirect("backend:question_add")
        else:
            messages.error(request,"Invalid formset")
            self.context['exams']=exams
            self.context['formset']=formset
            return render(request, self.template_name, self.context)

@login_required(login_url="login/")
def question(request, id):
    exam = Exam.objects.filter(id=id).first()
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
            "exam":exam,
            'page_name':"exam",
            'page_title':"Question"
            
            }
        return render(request,"backend/question.html",context)
    else:
        return redirect("content:exam")

@login_required(login_url="login/")
def exam_history(request):
    # Group by exam and calculate the correct/incorrect counts
    if request.method == "GET"  and 'examinee_id' in request.GET:
        examinee_id = request.GET['examinee_id']
        examinee = Examinee.objects.filter(id= examinee_id).first()
        responses = ExamineeResponse.objects.filter(examinee=examinee).select_related('question__exam', 'selected_choice')
        
    else:
        responses = ExamineeResponse.objects.all().select_related('question__exam', 'selected_choice')
        
    exams = {}
    for response in responses:
        examinee = response.examinee
        exam = response.question.exam
        
        examinee_id = examinee.id
        exam_id = exam.id
        if examinee_id not in exams:
            exams[examinee_id]={}
            if  exam_id not in exams[examinee_id]:
                exams[examinee_id][exam_id] = {
                    'examinee_name':examinee.name,
                    'exam_title': exam.title,
                    'total_questions': 0,
                    'correct_answers': 0,
                    'incorrect_answers': 0
                }
        else:
            if  exam_id not in exams[examinee_id]:
                exams[examinee_id][exam_id] = {
                    'examinee_name':examinee.name,
                    'exam_title': exam.title,
                    'total_questions': 0,
                    'correct_answers': 0,
                    'incorrect_answers': 0
                }
        exams[examinee_id][exam_id]['total_questions'] += 1
        if response.is_correct():
            exams[examinee_id][exam_id]['correct_answers'] += 1
        else:
            exams[examinee_id][exam_id]['incorrect_answers'] += 1
    
    context = {
        'page_name':"exam_history",
        'exams':exams,
        'page_title':"Exam History"
        
        
    }
    return render(request, "backend/exam-history.html", context)

@login_required(login_url="login/")
def results(request):
    if request.method == "GET":
        exam_id =  request.GET.get('exam_id')
        examinee_id = request.GET.get('examinee_id')
        
        examinee = get_object_or_404(Examinee, id=examinee_id)
        exam = get_object_or_404(Exam, id=exam_id)
        
        if exam.is_time_up() is True:
            messages.success(request, f"Wait for the exam to end: {exam.end_time}")
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
            'examinee':examinee,
            'page_title': 'Exam Results'
        }
    return render(request, "backend/result-details.html", context)

@login_required(login_url="login/")
def examinee_list(request):
    examinees = Examinee.objects.all()
    context = {
        'page_name': 'examinee_list',
        'page_title': "Examinee List",
        'examinees' : examinees
    }
    return render(request, "backend/examinee-list.html", context)

@login_required
def examinee_profile_page(request, id):
    examinee = Examinee.objects.filter(id=id).first()
    attended_exams_count = ExamineeResponse.objects.filter(examinee=examinee).values('question__exam').distinct().count()
    if examinee is None:
        messages.error(request, "Examinee Not Found")
        return redirect("backend:examinee_list")
    context = {
            'examinee':examinee,
            'page_title':"Examinee Profile",
            'attended_exams_count':attended_exams_count
            }
    return render(request,"backend/examinee-profile.html", context)

@login_required
def examinee_profile_update(request, id):

    examinee = Examinee.objects.filter(id=id).first()
    if request.method == 'POST':
        form = ExamineeUpdateForm(request.POST, request.FILES, instance=examinee)
        if form.is_valid():
            email = form.cleaned_data['email']
            form.save()
            request.session['is_logged_in'] = True
            request.session['user_email'] = email
            messages.success(request, "Profile Update Successfully")
            return redirect("content:profile_update")  # Redirect to a profile page or other relevant page
        else:
            messages.error(request, "Something is Wrong")
    else:
        form = ExamineeUpdateForm(instance=examinee)  # Pre-populate form with existing data

    return render(request, "backend/examinee-profile-update.html", {'form': form, 'examinee':examinee})



@method_decorator(login_required(login_url="login/"), name='dispatch')
class NotificationView(View):
    template_name = 'backend/notification.html'
    
    context = {}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = "notification"
        context["page_title"] = "Notification"
        return context
    
    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.all().order_by('-timestamp')
        examinees = Examinee.objects.all()
        self.context['notifications']=notifications
        self.context["page_title"] = "Notification"
        self.context["page_name"] = "notification"
        self.context["examinees"] = examinees
        
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message')
        receiver = request.POST.get('receiver')
        examinee = 0
        if receiver == '2':
            examinee = request.POST.get('student')
            notification = Notification(
                message=message,
                examinee_id=examinee)
            notification.save()
        elif receiver == '1':
            examinees = Examinee.objects.all()
            notifications = [
            Notification(message=message, examinee=single_examinee)
            for single_examinee in examinees
        ]
        Notification.objects.bulk_create(notifications)
            
        return render(request, self.template_name, self.context)

