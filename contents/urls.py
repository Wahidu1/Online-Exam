from django.urls import path
from . import views
app_name = "content"
urlpatterns = [
    path('',views.dashboard, name="dashboard"),
    path('profile/',views.profile_page, name='profile'),
    
    path('exams/',views.exam_cat, name="exam"),
    path('exams/<int:id>/',views.question, name="question"),
    path('exam-history/',views.exam_history, name="exam_history"),
    path('results/<int:exam_id>/',views.results, name="results"),
    path('results-submission/<int:exam_id>/',views.result_submission, name="result_submission"),
    
    path('message/<int:exam_id>/',views.messages_page, name="message"),
    path('profile-update  /',views.profile_update, name="profile_update"),
    path('logout/',views.logout, name="logout"),
    
    path("notification/",views.NotificationListView.as_view(),name="notification" ),
    path("notification/<int:pk>/",views.NotificationDetailView.as_view(),name="notification_details" )
    
    
    
    
    
]