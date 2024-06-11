from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Subscription(models.Model):
    pub = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pubs",default=None)
    sub = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subs",default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pub', 'sub'], name='unique_subscription')
        ]
    def __str__(self):
        return f'{self.sub.username} subscribed to {self.pub.username} at {self.date}'
