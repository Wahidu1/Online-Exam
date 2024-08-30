from django import forms
from .models import Examinee

class ExamineeUpdateForm(forms.ModelForm):
    class Meta:
        model = Examinee
        fields = ['name', 'email', 'father_name', 'education_qualification', 'phone', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'id':"name", 'placeholder': ''}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'id':"email",'placeholder': ''}),
            'father_name': forms.TextInput(attrs={'class':'form-control', 'id':"father_name",'placeholder': ''}),
            'education_qualification': forms.TextInput(attrs={'class':'form-control','id':"education_qualification", 'placeholder': ''}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'id':'phone', 'placeholder': ''}),
            'image': forms.ClearableFileInput(attrs={'class':'form-control-file', 'id':"image", 'placeholder': 'Upload Profile Picture'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['father_name'].required = False
        self.fields['education_qualification'].required = False
        self.fields['image'].required = False