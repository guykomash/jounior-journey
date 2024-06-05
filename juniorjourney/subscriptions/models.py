from django.db import models

# Create your models here.

class Subscription(models.Model):
    pub_id = models.IntegerField()
    pub_name = models.CharField(max_length=255)
    sub_id = models.IntegerField()
    sub_name = models.CharField(max_length=255)
    sub_time = models.DateTimeField()
    
    def __str__(self):
        return f'{self.sub_name} subscribed to {self.pub_name} at {self.sub_time}'
