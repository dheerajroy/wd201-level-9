from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    report_time = models.TimeField(null=True)
    last_report_sent = models.DateField(null=True)

    def __str__(self):
        return self.user.username
