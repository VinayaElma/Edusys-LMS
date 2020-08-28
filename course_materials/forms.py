from django import forms
from .models import CourseMaterial

class NewCourseMaterialForm(forms.ModelForm):
    coursematerial_no = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    document =  forms.FileField(required=False)

    class Meta:
        model = CourseMaterial
        fields = ['coursematerial_no', 'description', 'document']
