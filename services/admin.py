from django.contrib import admin
from .models import Service, Product, ActionLogs, Location, Datacenter, PCloud, SCloud


admin.site.register(Service)
admin.site.register(Product)
admin.site.register(ActionLogs)
admin.site.register(Location)
admin.site.register(Datacenter)
admin.site.register(PCloud)
admin.site.register(SCloud)
