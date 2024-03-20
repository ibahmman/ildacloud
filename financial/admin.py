from django.contrib import admin
from .models import Wallet, Exchange_USDT, Invoice


admin.site.register(Wallet)
admin.site.register(Exchange_USDT)
admin.site.register(Invoice)
