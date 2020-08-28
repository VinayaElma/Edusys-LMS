from django import forms
from .models import Announcement

class NewAnnouncementForm(forms.ModelForm):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    document = forms.FileField(required=False)

    class Meta:
        model = Announcement
        fields = ['title', 'description', 'document']