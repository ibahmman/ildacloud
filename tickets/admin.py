from django.contrib import admin
from .models import Department, Ticket, Message, Attach

admin.site.register(Department)
admin.site.register(Ticket)
admin.site.register(Message)
admin.site.register(Attach)