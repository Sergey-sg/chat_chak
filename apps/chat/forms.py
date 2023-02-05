from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    """model form of Message"""
    # roomId = forms.IntegerField()

    class Meta:
        model = Message
        fields = ('content',)