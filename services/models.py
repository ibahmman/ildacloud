from django.db import models
from django.contrib.auth.models import User


class Datacenter(models.Model):
    name = models.CharField(max_length=26, unique=True)
    tag = models.CharField(max_length=2, unique=True)


class Location(models.Model):
    name = models.CharField(max_length=26, unique=True)
    tag = models.CharField(max_length=2, unique=True)


class Product(models.Model):

    CURRENCY_CHOICES = [
        ('usdt', 'تتر'),
        ('irt', 'تومان'),
    ]

    name = models.CharField(max_length=20)
    price_amount = models.FloatField()
    price_currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0][0])

    def __str__(self) -> str:
        return f'{self.name} amount: {self.price_amount}/{self.price_currency}'


class PCloud(Product):
    datacenter = models.ForeignKey(Datacenter, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    ram = models.IntegerField()
    cpu = models.IntegerField()
    disc_space = models.IntegerField()
    traffic = models.IntegerField()
    bandwidth = models.IntegerField()


class Service(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در طی راه اندازی'),
        ('active', 'در حال کار'),
        ('suspended', 'نگهداری شده'),
        ('terminated', 'ئاک شده'),
    ]

    PERIOD_CHOICES = [
        ('hourly', 'ساعتی'),
        ('daily', 'روزانه'),
        ('mounthly', 'ماهیانه'),
    ]

    user = models.ForeignKey(User, models.DO_NOTHING)
    product_main = models.ForeignKey(Product, models.DO_NOTHING)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    reason = models.TextField(blank=True, null=True)
    period = models.CharField(max_length=8, choices=PERIOD_CHOICES, default=PERIOD_CHOICES[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    lastpay_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.product_main} (user: {self.user}) status: {self.status}'
    

class SCloud(Service):
    product_cloud = models.ForeignKey(PCloud, models.DO_NOTHING)
    cloud_id = models.TextField(blank=True, null=True)
    root_password = models.TextField(blank=True, null=True)


class ActionLogs(models.Model):
    ACTION_CHOICES = [
        ('stop', 'خاموش'),
        ('start', 'روشن'),
        ('restart', 'ریستارت'),
        ('rebuild', 'نصب سیستم عامل'),
        ('passwd', 'ویرایش پسورد'),
        ('ipv4', 'جایگزینی آی پی 4'),
        ('ipv6', 'جایگزینی آی پی 6'),
        ('more', 'دیگر کار ها'),
    ]
    service = models.ForeignKey(Service, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    action = models.CharField(max_length=7, choices=ACTION_CHOICES)
    text = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user} {self.action} {self.service}'
