from .models import Topic
from django import forms


class TopicFrom(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
