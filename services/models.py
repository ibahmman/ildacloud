from django.db import models


class Product(models.Model):

    CURRENCY_CHOICES = [
        ('usdt', 'تتر'),
    ]

    name = models.CharField(max_length=20)
    price_amount = models.FloatField()
    price_currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0][0])
