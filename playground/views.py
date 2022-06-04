from django.shortcuts import render
from .tasks import notify_customers


def say_hello(request):
    """
    The Celery task is executed when someone navigates
    to the view.

    NOTE: To run the task you MUST use the delay function!
    """
    notify_customers.delay('Hello awesome customer!')
    return render(request, 'hello.html', {'name': 'Celery'})
