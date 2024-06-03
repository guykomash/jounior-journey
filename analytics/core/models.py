from django.db import models

# Create your models here.

class UserLogin(models.Model):
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    login_time = models.DateTimeField()

    def __str__(self):
        return f'{self.username} logged in at {self.login_time}'
    
class JobApplication(models.Model):
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    application_date = models.DateField()
    
    def __str__(self):
        return f'{self.username} applied at {self.application_date}'

