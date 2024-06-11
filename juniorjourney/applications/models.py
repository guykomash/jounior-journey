from django.db import models
from django.contrib.auth.models import User

class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]


    company_name = models.CharField('Company',max_length=75)
    role = models.CharField('Role', max_length=75)
    job_description = models.TextField('Description')
    applied_date = models.DateTimeField("Applied at",auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.CharField('Status',max_length=50, choices=STATUS_CHOICES, default='applied')
    resume = models.FileField('Resume',upload_to='resumes/',blank=True)
    # CASCADE = if User is deleted, all of his posts deleted too.

    class Meta:
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.author} application to {self.company }"