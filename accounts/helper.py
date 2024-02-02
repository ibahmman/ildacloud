from django.core.mail import send_mail
from bahman.settings import EMAIL_HOST_USER


def send_email_verify(**kwargs):
    """
    kwargs keys: first_name, last_name, last_email, new_email, link, website
    """

    text = f'''
    Hi dear,{kwargs['first_name']} {kwargs['last_name']}.
    your request for change email is in progress, click on link for accept.
    changing {kwargs['last_email']} to {kwargs['new_email']}.

    link:
    {kwargs['link']}
    
    chelseru: {kwargs['website']}
    '''
    send_mail(subject='chelseru: verify email', message=text, from_email=EMAIL_HOST_USER, recipient_list=[kwargs['new_email']])


def send_email_recovery(**kwargs):
    """
    kwargs keys: first_name, last_name, last_email, new_email, link, website
    """
    
    text = f'''
    Hi dear,{kwargs['first_name']} {kwargs['last_name']}.
    your account email changed to {kwargs['new_email']}, click on link for recovery.

    link:
    {kwargs['link']}
    
    chelseru: {kwargs['website']}
    '''
    send_mail(subject='chelseru: recovery email', message=text, from_email=EMAIL_HOST_USER, recipient_list=[kwargs['last_email']])
