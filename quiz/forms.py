from django import forms
from django.forms import modelformset_factory
from .models import Quiz, Quiz_Question, Choice, StudentAnswer
from accounts.models import Subject


class AddQuizForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'id': 'datetimepicker'}), required=True)
  
    class Meta:
        model = Quiz
        fields = ('name', 'subject', 'date')
        labels = {
            'name': 'Quiz-Name',
            'subject': 'Subject',
            'date':'Date'
        }

    def __init__(self, user, *args, **kwargs):
        super(AddQuizForm, self).__init__(*args, **kwargs)
        
        sub = user.subjects.all()
        self.fields['subject'].queryset = sub 

class QuestionModelForm(forms.ModelForm):

    class Meta:
        model = Quiz_Question
        fields = ('question', )
        labels = {
            'question': 'question'
        }
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter question here',
                }
            )
        }


class QuestionForm(forms.ModelForm):
    is_correct = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ('choice', 'is_correct')
        labels = {
            'choice': 'choice',
            'is_correct': 'is_correct',
        }
        widgets = {
            'choice':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Choice here',
            }

            ) 
        }


ChoiceFormset = modelformset_factory(Choice, form=QuestionForm, extra=4, max_num=4)


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Choice.objects.none(),
        widget=forms.RadioSelect(attrs={'class': 'form-control'}),
        required=True,
        empty_label=None)

    class Meta:        
        model = StudentAnswer
        fields = ('answer', )
        
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('choice')
