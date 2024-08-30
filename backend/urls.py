from django.urls import path
from . import views 
app_name = "backend"
urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    
    path('exam-add/',views.exam_add, name='exam_add'),
    path('exam-list/',views.exam_list, name='exam_list'),
    path('exam-edit/<int:exam_id>/',views.exam_edit, name='exam_edit'),
    
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.logout_page, name='logout'),
    
    path('question-add/', views.QuestionAddView.as_view(), name='question_add'),
    path('question/<int:id>/', views.question, name='question'),
    
    path('exam-history/', views.exam_history, name='exam_history'),
    path('result-details/', views.results, name='results'),
    
    path('examinee-list/',views.examinee_list, name='examinee_list'),
    path('examinee-profile/<int:id>/',views.examinee_profile_page, name='examinee_profile_page'),
    path('examinee-profile-update/<int:id>/',views.examinee_profile_update, name='examinee_profile_update'),
    
    path('notification/', views.NotificationView.as_view(), name='notification'),
    
    
    
    
    
    
    
    
    
]