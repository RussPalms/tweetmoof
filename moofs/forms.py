from django.conf import settings
from django import forms
from .models import Moof

MAX_MOOF_LENGTH = settings.MAX_MOOF_LENGTH

class MoofForm(forms.ModelForm):
    class Meta:
        model = Moof
        fields = ['content']
        
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_MOOF_LENGTH:
            raise forms.ValidationError("This moof is too long")
        return content
