from django import forms
from forum.models import Topic


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
         widget=forms.Textarea(attrs={'rows': 7, 'placeholder': 'Ask your question here'}),
         max_length=4000,
         # help_text='The maximum length allowed is 4000'
         )

    class Meta:
        model = Topic
        fields = ['description', 'message', 'document']
