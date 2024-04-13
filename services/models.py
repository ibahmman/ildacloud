from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from clouds.cpanel import HZCloud


class Datacenter(models.Model):
    name = models.CharField(max_length=26, unique=True)
    tag = models.CharField(max_length=2, unique=True)

    def __str__(self) -> str:
        return f'{self.name}  {self.tag}'


class Location(models.Model):
    name = models.CharField(max_length=26, unique=True)
    tag = models.CharField(max_length=2, unique=True)

    def __str__(self) -> str:
        return f'{self.name}  {self.tag}'


class Product(models.Model):
    CURRENCY_CHOICES = [
        ('usdt', 'تتر'),
    ]

    name = models.CharField(max_length=20, unique=True)
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

    # class Meta:
    #     unique_together = ['datacenter', 'location', 'name']


class Service(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در طی راه اندازی'),
        ('active', 'در حال کار'),
        ('suspended', 'نگهداری شده'),
        ('terminated', 'پاک شده'),
    ]

    PERIOD_CHOICES = [
        ('hourly', 'ساعتی'),
        ('daily', 'روزانه'),
        ('monthly', 'ماهیانه'),
    ]

    user = models.ForeignKey(User, models.DO_NOTHING)
    product_main = models.ForeignKey(Product, models.DO_NOTHING)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    reason = models.TextField(blank=True, null=True)
    period = models.CharField(max_length=8, choices=PERIOD_CHOICES, default=PERIOD_CHOICES[0][0])
    uptime = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    lastpay_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.product_main} (user: {self.user}) status: {self.status}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self):
        return super(Service, self).delete()
    
    def change_type(self, product):
        try:
            product = Product.objects.get(name=product)
            self.product_main = product
            self.save()
        except:
            return False
        else:
            return True

    def last_pay_update(self):
        amount = self.product_main.price_amount
        if self.period == 'hourly': amount = self.product_main.price_amount / 30 / 24
        elif self.period == 'daily': amount = self.product_main.price_amount / 30
        elif self.period == 'monthly': amount = self.product_main.price_amount
        if self.user.wallet.reduce_balance(amount):
            self.lastpay_at = now()
            self.save()

            # if not self.delivered_at:
            #     self.deliver()

    def deliver(self, *args, **kwargs):
        self.delivered_at = now()
        self.save()


class SCloud(Service):
    product_cloud = models.ForeignKey(PCloud, models.DO_NOTHING)
    cloud_id = models.TextField(blank=True, null=True)
    cloud_ipv4 = models.TextField(max_length=15, blank=True, null=True)
    cloud_ipv6 = models.TextField(max_length=39, blank=True, null=True)
    root_password = models.TextField(blank=True, null=True)

    def deliver(self, *args, **kwargs):
        if self.product_cloud.datacenter.tag == 'HZ':
            try:
                cloud = HZCloud()
                cloud = cloud.create_a_server(**kwargs)
                assert 'id' in cloud['server'], 'server do not to create in datacenter.'
                self.cloud_id = cloud['server']['id']
                self.root_password = cloud['root_password']
                self.save()
                return cloud
            except AssertionError as e:
                return {'error': str(e)}
            except:
                return {'error': 'exception in create cloud and deliver.'}

    def delete(self):
        if self.product_cloud.datacenter.tag == 'HZ':
            try:
                cloud = HZCloud(server_id=self.cloud_id)
                cloud = cloud.delete_a_server()
                assert "id" in cloud["action"], 'can not to delete server.'
                super(SCloud, self).delete()
                return cloud
            except AssertionError as e:
                return {'error': str(e)}
            except:
                return {'error': 'exception in delete server.'}

    def change_type(self, product):
        if super().change_type(product.upper()):
            try:
                product_cloud = PCloud.objects.get(name=product.upper())
                self.product_cloud = product_cloud
                self.save()
            except:
                return False
            else:
                cloud = HZCloud(server_id=self.cloud_id)
                response = cloud.change_type_server(product_cloud.name.lower())
                print(response)
                return response
                # return True

    def hetzner_actions(self, action, more=None):
        response = {'error': ':)'}
        match action:
            case 'stop':
                # stop
                hzcloud = HZCloud(server_id=self.cloud_id)
                response = hzcloud.power_off_server()
            case 'shutdown':
                # shutdown
                hzcloud = HZCloud(server_id=self.cloud_id)
                response = hzcloud.shutdown_server()
            case 'start':
                # start
                hzcloud = HZCloud(server_id=self.cloud_id)
                response = hzcloud.power_on_server()
            case 'reboot':
                # reboot
                hzcloud = HZCloud(server_id=self.cloud_id)
                response = hzcloud.hard_restart_server()
            case 'restart':
                # restart
                hzcloud = HZCloud(server_id=self.cloud_id)
                response = hzcloud.soft_reboot_server()
            case 'rebuild':
                # rebuild
                hzcloud = HZCloud(server_id=self.cloud_id)
                response = hzcloud.rebuild_server(more)
            case 'passwd':
                # passwd
                hzcloud = HZCloud(server_id=self.cloud_id)
                response = hzcloud.reset_passwd_server()
                # need for set to model (cloud) and save.
                self.root_password = response['root_password']
                self.save()
            case 'ipv4':
                # ipv4
                pass
            case 'ipv6':
                # ipv6
                pass
            case 'ptr4':
                # ptr4
                hzcloud = HZCloud(server_id=self.cloud_id)
                response = hzcloud.change_ptr(dns_ptr=more)
            case 'console':
                # console
                hzcloud = HZCloud(server_id=self.cloud_id)
                response = hzcloud.request_console_server()
        return response


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
