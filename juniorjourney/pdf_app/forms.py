from . import models
from django import forms

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = models.PDFFile
        fields = ['file']