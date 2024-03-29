from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    referral = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='referral', blank=True, null=True)

    def __str__(self):
        return f'{self.user} {self.mobile}'

