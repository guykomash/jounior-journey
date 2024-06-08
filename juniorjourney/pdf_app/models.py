from django.db import models

# Create your models here.

class PDFFile(models.Model):
    file = models.FileField(upload_to='pdfs/')
    file_name = models.CharField(max_length=50)
    user_id = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)