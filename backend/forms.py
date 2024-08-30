from django import forms
from contents.models import Exam, Question, Choice

from django import forms
from users.models import Examinee
from datetime import datetime


class ExamForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': "start_date", 'type': 'date'})
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'id': "start_time", 'type': 'time'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': "end_date", 'type': 'date'})
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'id': "end_time", 'type': 'time'})
    )

    class Meta:
        model = Exam
        fields = ['title', 'description', 'start_date', 'start_time', 'end_date', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': "name", 'placeholder': ''}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'id': "description", 'placeholder': ''}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        
        if self.instance and self.instance.id:
            self.fields['start_date'].initial = self.instance.start_time.date()
            self.fields['start_time'].initial = self.instance.start_time.time()
            self.fields['end_date'].initial = self.instance.end_time.date()
            self.fields['end_time'].initial = self.instance.end_time.time()

    def clean(self):
        cleaned_data = super().clean()

        # Get the date and time inputs
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        end_date = cleaned_data.get('end_date')
        end_time = cleaned_data.get('end_time')

        if start_date and start_time:
            # Concatenate start date and time
            cleaned_data['start_time'] = datetime.combine(start_date, start_time)
        if end_date and end_time:
            # Concatenate end date and time
            cleaned_data['end_time'] = datetime.combine(end_date, end_time)

        return cleaned_data
    
class MCQAddForm(forms.Form):
    CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
    ]
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.all(),
        widget=forms.HiddenInput(attrs={'id': "exam"})  
    )
    question = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': "question" , 'placeholder':"Enter Question "})
    )
    choice_1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': "choice_1" , 'placeholder':"Enter Option 1"})
    )
    choice_2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': "choice_2" , 'placeholder':"Enter Option 2"})
    )
    choice_3 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': "choice_3" , 'placeholder':"Enter Option 3"})
    )
    choice_4 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': "choice_4" , 'placeholder':"Enter Option 4"})
    )
    correct_answer = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select', 'id': "correct_answer"}),
        choices=CHOICES,
    )

    def save(self):
        # Create the Question instance
        question_instance = Question.objects.create(
            exam=self.cleaned_data['exam'],
            text=self.cleaned_data['question']
        )

        # Prepare the choices
        choices_data = [
            {'text': self.cleaned_data['choice_1']},
            {'text': self.cleaned_data['choice_2']},
            {'text': self.cleaned_data['choice_3']},
            {'text': self.cleaned_data['choice_4']},
        ]

        correct_answer_index = int(self.cleaned_data['correct_answer']) - 1
        
        # Create Choice instances
        choice_instances = []
        for i, choice_data in enumerate(choices_data):
            choice_instances.append(
                Choice.objects.create(
                    question=question_instance,
                    text=choice_data['text'],
                    is_correct=(i == correct_answer_index)
                )
            )
        
        return question_instance, choice_instances


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