from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Profile, User, VerifySMSCode


class SMSForm(forms.Form):
    mobile = forms.CharField(max_length=11, min_length=11, required=True, help_text='09xxxxxxxxx')
    code = forms.CharField(max_length=6, min_length=6, required=False)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', )


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class UpdateEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio')


class UpdateMobileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('mobile', )










# class UserPowerForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super(UsePowerForm, self).__init__(*args, **kwargs)

#         player = Player.objects.get(id=self.initial['player'])

#         ###from here you can use player to get the power policies and put into list

#         self.fields['power_policy'] = forms.ChoiceField(choices=power_policy_list)


#     class Meta:
#         model = UserPower
#         fields = ['player', 'power_policy']