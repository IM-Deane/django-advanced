from time import sleep
from celery import shared_task

"""
NOTE: The shared_task decorator is used instead of is used in place of our
specific celery instance (ie. from storefront.celery import celery) to
decouple it from the storefront.

This ensures that storefront isn't needed when using celery in other apps.

Gotta keep things modular.
"""

@shared_task
def notify_customers(message):
    """
    Adding the decorator tells Celery that we want it
    to execute this task asynchronously.

    NOTE: Check out playground/views.py to learn how
    to run the task.
    """
    print('Sending 10k emails...')
    print(message)
    sleep(10) # simulate intensive operation
    print('Emails were successfully sent!')
