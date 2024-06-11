from django import forms
from . import models

class CreateApplication(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['company_name', 'role', 'job_description','resume']