from django import forms
from .models import Assignment, Question, DescriptiveResult


class NewAssignmentForm(forms.ModelForm):
    assignment_no = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'id': 'datetimepicker'}), required=False)

    class Meta:
        model = Assignment
        fields = ['assignment_no', 'description', 'due_date']


class NewFileUploadForm(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Question
        fields = ['question', 'document', 'marks']


class NewSubmissionForm(forms.ModelForm):
    document = forms.FileField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = DescriptiveResult
        fields = ['document', 'description']


class NewMarksForm(forms.ModelForm):
    class Meta:
        model = DescriptiveResult
        fields = ['marks']
    
    def clean(self):
        marks=self.cleaned_data.get('marks')
        if marks and self.instance.question.marks < marks :
            raise forms.ValidationError({'marks':'marks should be less than maximum marks'})
        if marks < 0 :
            raise forms.ValidationError({'marks':'marks should be greater than 0'})