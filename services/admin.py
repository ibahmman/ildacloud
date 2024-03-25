from django.contrib import admin
from .models import Datacenter, Location, Product, PCloud, Service, SCloud, ActionLogs

admin.site.register(Datacenter)
admin.site.register(Location)
admin.site.register(Product)
admin.site.register(PCloud)
admin.site.register(Service)
admin.site.register(SCloud)
admin.site.register(ActionLogs)
