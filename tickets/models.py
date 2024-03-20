from django.db import models
from django.contrib.auth.models import User
from services.models import Service


class Department(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Ticket(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    service = models.ForeignKey(Service, models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey(Department, models.DO_NOTHING)
    subject = models.CharField(max_length=35)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.service} - {self.department} - {self.subject}'


class Message(models.Model):
    TYPE_CHOICES = [
        ('reply', 'پاسخ'),
        ('note', 'نوت')
    ]

    user = models.ForeignKey(User, models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, models.CASCADE)
    text = models.TextField()
    type = models.CharField(max_length=5, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.type} - {self.text}'


class Attach(models.Model):
    message = models.ForeignKey(Message, models.CASCADE)
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.message.text} - {self.file}'
