from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    """model form of Message"""

    class Meta:
        model = Message
        fields = ('content', 'room')