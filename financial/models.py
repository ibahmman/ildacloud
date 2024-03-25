from django.db import models
from django.contrib.auth.models import User
from services.models import Product, PCloud, Service, SCloud


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, primary_key=True)
    usdt = models.FloatField(default=0.0)
    earning = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user} (usdt:{self.usdt}) (earning:{self.earning})'


class Exchange_USDT(models.Model):
    FINANCIAL_UNIT_CHOICES = [
        ('irr', 'ریال'),
        ('irt', 'تومان'),
    ]
    to_unit = models.CharField(max_length=5, choices=FINANCIAL_UNIT_CHOICES)
    amount = models.FloatField()

    def __str__(self) -> str:
        return f'{self.amount} {self.get_display_to_unit()}'


class Invoice(models.Model):
    TYPE_CHOICES = [
        (1, 'Purchase Invoice'),
        (2, 'Renewal invoice'),
        (3, 'Extension invoice'),
    ]

    PAYMENT_CHOICES = [
        (0, 'Wallet'),
        (1, 'Unipayment'),
        (2, 'IDPay'),
    ]

    STATUS_CHOICES = [
        (1, 'New'),
        (2, 'Complete'),
        (3, 'Expired'),
    ]

    service = models.ForeignKey(Service, models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    itype = models.IntegerField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0])
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    payment_handler = models.IntegerField(choices=PAYMENT_CHOICES, default=PAYMENT_CHOICES[0][0])
    payment_id = models.TextField(blank=True, null=True)
    payment_url = models.SlugField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.service.user} (service:{self.service.id}) (product:{self.product})'
