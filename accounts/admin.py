from django.contrib import admin
from .models import Wallet, Admin, Profile, VerifyEmailToken, RecoveryEmailToken, VerifySMSCode

admin.site.register(Wallet)
admin.site.register(Admin)
admin.site.register(Profile)
admin.site.register(VerifyEmailToken)
admin.site.register(RecoveryEmailToken)
admin.site.register(VerifySMSCode)

