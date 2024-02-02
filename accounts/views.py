from typing import Any, Dict, Optional
from django import http
from django.db import models
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout, hashers
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, RedirectView, DetailView, View, FormView
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.utils.timezone import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import random, string
from .models import User, Profile, VerifyEmailToken, RecoveryEmailToken, VerifySMSCode
from .forms import UserLogin, UserForm, SMSForm, UpdateUserForm, UpdateProfileForm, UpdateEmailForm, UpdateMobileForm


# ------------------ PROFILE/USER VIEWS ------------------
class ProfileCreate(CreateView):
    template_name = '_profiles/query-user.html'
    model = User
    form_class = UserForm

    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('_profiles:index'))

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        Profile(user=user).save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self) -> str:
        return reverse('_profiles:index')


class UserLogin(FormView):
    form_class = UserLogin
    template_name = '_profiles/query-user.html'

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_active:
            return HttpResponseRedirect(reverse('_profiles:index'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form) -> HttpResponse:
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
            else:
                return HttpResponse('Inactive user.')
        return HttpResponseRedirect(reverse('_profiles:login'))


#
# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return HttpResponseRedirect(reverse('_profiles:login'))


class ProfileView(DetailView):
    template_name = '_profiles/index.html'
    model = Profile
    pk_url_kwarg = 'username'

    def get_object(self):
        print(self.request.user.username)
        return get_object_or_404(Profile, user__username=self.request.user.username)

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_active and self.get_object() == request.user.profile:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('_profiles:login'))


class UpdateUser(UpdateView):
    template_name = '_profiles/update-user.html'
    model = User
    form_class = UpdateUserForm
    pk_url_kwarg = 'username'
    success_url = '/my'

    def get_object(self):
        return get_object_or_404(self.model, username=self.kwargs[self.pk_url_kwarg])

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_active and self.get_object() == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('_profiles:login'))
    

class UpdateProfile(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = '_profiles/update-profile.html'
    pk_url_kwarg = 'username'

    def get_object(self):
        return get_object_or_404(self.model, user__username=self.kwargs[self.pk_url_kwarg])

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_active and self.get_object().user == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('_profiles:login'))    


# ------------------    EMAIL  VIEWS    ------------------
class UpdateEmail(UpdateView):
    model = User
    form_class = UpdateEmailForm
    template_name = '_profiles/update-email.html'
    pk_url_kwarg = 'username'

    def get_object(self):
        return get_object_or_404(self.model, username=self.kwargs[self.pk_url_kwarg])

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_active and self.get_object() == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('_profiles:login'))

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        Profile.objects.filter(user=self.get_object()).first().change_email_request(new_email=form.cleaned_data['email'])
        return HttpResponseRedirect(reverse('_profiles:index'))
    

class VerifyEmail(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        try:
            verify_token = VerifyEmailToken.objects.get(token=kwargs['token'])
            verify_token.change_email_finish()
            profile = verify_token.profile
            return profile.get_absolute_url()
        except:
            pass

        return super().get_redirect_url(*args, **kwargs)


class RecoveryEmail(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        try:
            recovery_token = RecoveryEmailToken.objects.get(token=kwargs['token'])
            recovery_token.recovery_email_finish()
            profile = recovery_token.profile
            return profile.get_absolute_url()
        except:
            pass

        return super().get_redirect_url(*args, **kwargs)


# ------------------    MOBILE VIEWS    ------------------
class SMSAuth(FormView):
    template_name = '_profiles/sms.html'
    form_class = SMSForm

    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('_profiles:index'))

    def form_valid(self, form: Any) -> HttpResponse:
        if 'sendcode' in self.request.POST:
            VerifySMSCode(mobile=form.cleaned_data['mobile']).save()
            return self.render_to_response(self.get_context_data(form=form))
        else:
            try:
                obj = VerifySMSCode.objects.filter(mobile=form.cleaned_data['mobile']).filter(code=form.cleaned_data['code']).first()
                assert obj, 'verify code and mobile is not match or exist.'
                
                # login.
                profile = obj.get_profile()
                if profile is not False:
                    # user = authenticate(self.request, username=profile.user.username)
                    user = get_object_or_404(User, username=profile.user.username)
                    if user is not None:
                        if user.is_active:
                            login(self.request, user)
                        else:
                            return HttpResponse('Inactive user.')
                else:
                    # signup
                    if obj.sign_up():
                        # login after signup.
                        user = get_object_or_404(User, username= obj.get_profile().user.username)
                        if user is not None:
                            if user.is_active:
                                login(self.request, user)
                            else:
                                return HttpResponse('Inactive user.')
                return HttpResponseRedirect(self.get_success_url())
                    
            except AssertionError as e:
                print(e)
            #   refresh current page with form context.
            return self.render_to_response(self.get_context_data(form=form))    
    
    def get_success_url(self) -> str:
        return reverse('_profiles:index')
        # return HttpResponseRedirect(self.request.GET['HTTP_REFERER'])


class UpdateMobile(UpdateView):
    model = Profile
    form_class = UpdateMobileForm
    template_name = '_profiles/update-mobile.html'
    pk_url_kwarg = 'username'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs[self.pk_url_kwarg])

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_active and self.get_object() == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('_profiles:login'))

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.request.user.profile.change_mobile_request(form.cleaned_data['mobile'])
        
        return HttpResponseRedirect(reverse('_profiles:index'))
        

    pass
