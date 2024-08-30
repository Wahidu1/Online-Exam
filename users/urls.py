from django.urls import path
from .views import register, login, otp_verify
app_name = "user"
urlpatterns = [
    path("register/",register,name="register"),
    path("login/",login,name="login"),
    path("otp/",otp_verify,name="otp"),
    
    
]