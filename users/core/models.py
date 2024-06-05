from django.db import models

# Create your models here.

class Subscription(models.Model):
    user_id = models.IntegerField()
    sub_id  = models.IntegerField()
    sub_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.sub_id} subscribed to {self.user_id}"
