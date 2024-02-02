# from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
from django.utils.timezone import datetime, timedelta, now
from django.contrib.sites.models import Site
from django.urls import reverse
# from django.http import HttpResponseRedirect
from . import helper, smsmanage
import string

from random import randint, choice


class Wallet(models.Model):
    profile = models.OneToOneField('Profile', models.CASCADE)
    tomans = models.IntegerField(default=0)

    def __str__(self):
        return self.profile.__str__()


class Admin(models.Model):
    profile = models.OneToOneField('Profile', models.CASCADE)

    def __str__(self):
        return self.profile.__str__()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # wallet = models.OneToOneField('Wallet', models.SET_NULL, blank=True, null=True)
    mobile = models.CharField('Mobile', max_length=11, unique=True, blank=True, null=True)
    avatar = models.ImageField('Avatar', width_field='125', height_field='125', upload_to='avatars/',
                               blank=True, null=True)
    bio = models.CharField('Bio', max_length=116, blank=True, null=True)
    last_update_mobile = models.DateTimeField('Last Update Mobile', blank=True, null=True)
    last_update_email = models.DateTimeField('Last Update Emails', blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user}'

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            Wallet(profile=self).save()
            return True
        except:
            return False

    def get_absolute_url(self):
        return reverse('_profiles:index')

    def change_email_request(self, new_email):
        return VerifyEmailToken(profile=self, email=new_email).save()

    def send_mobile_code(self, mobile):
        return VerifySMSCode(mobile=mobile).save()
    
    def change_mobile_request(self, new_mobile):
        if self.user.username == self.mobile:
            self.user.username = new_mobile
            self.user.save()
        self.mobile = new_mobile
        self.save()
        # return VerifySMSCode(mobile=new_mobile, profile=self).save()
    

class VerifyEmailToken(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField('Email')
    token = models.SlugField('Token', unique=True)

    create_at = models.DateTimeField('Create at', auto_now_add=True)
    expiration_at = models.DateTimeField('Expiration at', blank=True, null=True)

    def change_email_finish(self):
        try:
            assert self.expiration_at.timestamp() >= now().timestamp(), 'verify email token expirated.'
        except AssertionError as e:
            self.delete()
            print('Error: AP-M-VE-03', e, sep='\n')
        except:
            print('Error: AP-M-VE-04')
        
        else:
            try:
                # if self.profile.user.email:
                recovery_email = RecoveryEmailToken(profile=self.profile, email=self.profile.user.email)
                self.profile.user.email = self.email
                self.profile.user.save()
                self.profile.lastupdate_email = now()
                self.profile.save()
                self.delete()
            except:
                print('Error: AP-M-VE-05')
            else:
                # if recovery_email:
                recovery_email.save()

    def save(self, *args, **kwargs):
        email_to = self.profile.user.email
        try:
            assert email_to, 'Email_to is null.'
            assert (self.profile.lastupdate_email + timedelta(days=7)).timestamp() <= datetime.now().timestamp(), \
                'last update of email most gte 7 days.'

            letters = string.ascii_letters
            token = ''.join(choice(letters) for _ in range(40))
            instances = (VerifyEmailToken.objects.filter(token=token) |
                         VerifyEmailToken.objects.filter(profile=self.profile) |
                         VerifyEmailToken.objects.filter(email=self.email))
            if instances:
                instances.delete()
            
            # make new token ans save().
            self.token = token
            self.expiration_at = now() + timedelta(hours=2)
            super().save(*args, **kwargs)
            
            # send email.
            first_name = self.profile.user.first_name
            last_name  = self.profile.user.last_name
            last_email = self.profile.user.email
            params = {
                'first_name': first_name if first_name else '-',
                'last_name' : last_name if last_name else 'user',
                'last_email': last_email if last_email else 'has no email',
                'new_email' : self.email,
                'link'     : str(Site.objects.get_current().domain) + str(reverse('_profiles:verify-email',
                                                                                  args=[self.token])),
                'website'  : Site.objects.get_current().name
            }
            helper.send_email_verify(**params)
            return True
        
        except AssertionError as e:
            print('Error: AP-M-VE-01', e, sep='\n')
        except:
            print('Error: AP-M-VE-02', sep='\n')

        return False
    

class RecoveryEmailToken(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField('Email')
    token = models.SlugField('Token', unique=True)

    create_at = models.DateTimeField('Create at', auto_now_add=True)
    expiration_at = models.DateTimeField('Expiration at', blank=True, null=True)

    def recovery_email_finish(self):
        try:
            assert self.expiration_at.timestamp() >= now().timestamp(), 'verify email token expirated.'
        except AssertionError as e:
            self.delete()
            print('Error: AP-M-RE-03', e, sep='\n')
        except:
            print('Error: AP-M-RE-04')
        
        else:
            try:
                self.profile.user.email = self.email
                self.profile.user.save()
                self.profile.lastupdate_email = now()
                self.profile.save()
                self.delete()
            except:
                print('Error: AP-M-RE-05')

    def save(self, *args, **kwargs):
        email_to = self.email
        try:
            assert email_to, 'Email_to is null.'
            letters = string.ascii_letters
            token = ''.join(choice(letters) for _ in range(40))
            instances = (RecoveryEmailToken.objects.filter(token=token) |
                         RecoveryEmailToken.objects.filter(profile=self.profile) |
                         RecoveryEmailToken.objects.filter(email=self.email))
            if instances:
                instances.delete()

            # make new token ans save().
            self.token = token
            self.expiration_at = now() + timedelta(days=7)
            super().save(*args, **kwargs)

            # send email.
            first_name = self.profile.user.first_name
            last_name  = self.profile.user.last_name
            new_email = self.profile.user.email
            params = {
                'first_name': first_name if first_name else '-',
                'last_name' : last_name if last_name else 'user',
                'last_email': self.email,
                'new_email' : new_email if new_email else 'has no email',
                'link'     : str(Site.objects.get_current().domain) + str(reverse('_profiles:recovery-email',
                                                                                  args=[self.token])),
                'website'  : Site.objects.get_current().name
            }
            helper.send_email_recovery(**params)
            return True
        
        except AssertionError as e:
            print('Error: AP-M-RE-01', e, sep='\n')
        except:
            print('Error: AP-M-RE-02', sep='\n')

        return False
    

class VerifySMSCode(models.Model):
    mobile = models.CharField('Mobile', max_length=11, unique=True)
    code = models.IntegerField('Code')
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    create_at = models.DateTimeField('Create at', auto_now_add=True)
    expiration_at = models.DateTimeField('Expiration at', blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.mobile} - {self.code}'

    def sign_up(self):
        letters = string.ascii_letters
        password = ''.join(choice(letters) for _ in range(25))
        try:
            assert not Profile.objects.filter(mobile=self.mobile), 'mobile is unavailable.'
            user, create = User.objects.get_or_create(username=self.mobile)
            if create:
                user.set_password(password)
                user.save()
                print(user)
                Profile(user=user, mobile=self.mobile).save()
                return True

        except AssertionError as e:
            print(e)
        return False

    def get_profile(self):
        try:
            obj = Profile.objects.filter(mobile=self.mobile)
            assert obj, 'user not found with mobile.'
            return obj.first()
        except AssertionError as e:
            print(e)
        return False

    # def change_mobile_finish(self):
    #     try:
    #         assert self.expiration_at.timestamp() >= now().timestamp(), 'code expirated.'
    #     except AssertionError as e:
    #         self.delete()
    #         print('Error: AP-M-VM-01', e, sep='\n')
    #     except:
    #         print('Error: AP-M-VM-02')
        
    #     else:
    #         try:
    #             self.profile.mobile = self.mobile
    #             if self.profile.user.username == self.profile.mobile:
    #                 self.profile.user.username = self.mobile
    #                 self.profile.user.save()
    #             self.profile.save()
    #             self.delete()
    #         except:
    #             print('Error: AP-M-VM-03')

    def save(self, *args, **kwargs):
        instance = VerifySMSCode.objects.filter(mobile=self.mobile)
        if instance and now().timestamp() > instance.first().expiration_at.timestamp():
            instance.delete()

        if not instance:
            # have not any instanse as mobile in table.
            code = str(randint(100000, 999999))
            sms = smsmanage.ParsianWeb(mobile=self.mobile)
            smsresponse = sms.send_code(code)

            if smsresponse['status'] == 200:
                self.code = code
                self.expiration_at = now() + timedelta(seconds=140)
                super().save(*args, **kwargs)
                return {'message': 'successfully.', 'status': smsresponse['status']}

            return {'message': 'sms service error.', 'status': smsresponse['status']}
        return {'message': 'try again after 2 minutes.'}

