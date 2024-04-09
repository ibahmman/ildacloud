from celery import shared_task

@shared_task
def p():
    print('hello world')