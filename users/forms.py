from django import forms
from .models import Examinee

class ExamineeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Examinee
        fields = ['name', 'email', 'father_name', 'education_qualification', 'phone', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'id':"name", 'placeholder': 'নাম লিখুন'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'id':"email",'placeholder': 'ইমেইল লিখুন'}),
            'father_name': forms.TextInput(attrs={'class':'form-control', 'id':"father_name",'placeholder': 'পিতার নাম লিখুন'}),
            'education_qualification': forms.TextInput(attrs={'class':'form-control','id':"education_qualification", 'placeholder': 'শিক্ষাগত যোগ্যতা লিখুন'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'id':'phone', 'placeholder': 'মোবাইল নাম্বার লিখুন'}),
            'image': forms.ClearableFileInput(attrs={'class':'.form-control-file', 'id':"image", 'placeholder': 'ছবি আপলোড'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['father_name'].required = False
        self.fields['education_qualification'].required = False
        self.fields['image'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Examinee.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Examinee.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone


class ExamineeLoginForm(forms.Form):
        email = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'ইমেইল লিখূন',
            'autofocus': 'autofocus', 
        })
    )
class ExamineeOTPForm(forms.Form):
        digit1 = forms.CharField(
        max_length=1,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'digit1',
            'placeholder': '',
        })
    )
        digit2 = forms.CharField(
        max_length=1,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'digit2',
            'placeholder': '',
        })
    )
        digit3 = forms.CharField(
        max_length=1,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'digit3',
            'placeholder': '',
        })
    )
        digit4 = forms.CharField(
        max_length=1,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'digit4',
            'placeholder': '',
        })
    )

