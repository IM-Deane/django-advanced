# Running Background Tasks with Celery

## Description

This project was created while following
[codewithmosh.com's](https://codewithmosh.com/p/the-ultimate-django-series)
Ultimate Django Series.

In part 3, we learn about advanced concepts regarding Django utilities.

This branch contains the section on running async tasks using
[celery](https://docs.celeryq.dev/en/stable/)

Even though i've worked with Django professionally, working with celery is
something I found confusing at times.

The purpose of this repo is to act as reference when implementing it future
projects.

### What is Celery

When you need to perform intensive secondary tasks such as image processing,
emails, or data modeling, you should use an async operation. These types of
operations allow you to delegate various tasks to other processes and keep your
app available for its primary purpose.

Celery is a library that allows you to easily manage these async tasks.

When you wish to perform a task in the background, you pass it to Celery's queue
which will then assign the task to a worker.

You can have as many workers as you need to perform tasks. Once a Celery worker
has finished, it will notify your app that the task has been completed.

Another benefit of offloading tasks to Celery is that if a task happens to fail,
it won't impact the rest of your app. This enables smoother error handling and a
better user experience.

### Message Brokers

The Celery queue is a message broker/middleman that is responsible for passing
tasks to workers.

If there are no workers available, the broker will wait until one is free. This
ensures that the task will be completed as soon as possible.

**Django Message Brokers:** The two most popular Django brokers are Redis and
RabbitMQ.

Redis: If you've used Redis before, you know that its actually an in-memory data
store, but can also act as a message broker. Besides acting as a broker, Redis
is also a popular caching option.

RabbitMQ: An enterprise-grade message broker that is great for larger projects.

In the course we used Redis as our broker because of how easy it is to setup.

As a general rule, its best to avoid over-engineering your applications.

Start with something simple and then gradually upgrade your infrastructure as
your needs progress.

### Installing Redis

We used a Docker container to get Redis running on our local machine at
port 6379.

**Running Redis** To run the container, open a terminal in the root of the
project and type the following command: `docker run -d -p 6379:6379 redis`

This pulls the Redis image from DockerHub and spins up a container mapped to
**port 6379** of your computer.

Note: `docker run -d` will start the container in detached mode. Which means it
runs in the background.

To verify that the redis is running, you can use `docker ps` which list's all
containers running on your machine.

If you see 'redis' in the IMAGE column then you're good to go!

**Redis and Django** Finally, we need to add Redis to Django's list of
dependencies: `pipenv install redis`

**NOTE:** Redis should already be present in the dependencies but I left this
here as a reference for when you're working with a new project.

### Setting up Celery

\*\* Windows Users Beware: The following section demonstrates how to setup
Celery for Mac and Linux computers. If you're using Windows then you should be
aware that Celery has
[dropped support for Windows](https://docs.celeryq.dev/en/stable/faq.html#does-celery-support-windows)
as of version 4.xx.

However, a quick internet search shows there are several workarounds. This
tutorial should get you started https://www.youtube.com/watch?v=t2ZoVlqlQyA.

**Installing Celery** From your terminal, add celery to your Django
dependencies: `pipenv install celery`

Once that's installed you can navigate to whichever directory you'd like to work
with celery.

For this project, we're using the **storefront** folder. Take a look at the
**celery.py** file to learn how to the setup works.

### Running Celery

To start celery, use the following command:
`celery -A storefront worker --loglevel=info`

> -A storefront is your project worker is the type of process you're
> initializing --loglevel=info runs celery in debug mode which displays logs in
> the terminal

### Creating & Executing Tasks

Getting Celery to run a task is as simple as adding a decorator to any functions
you want executed in the background.

For this project, take a look at `playground/tasks.py` for details on how to
create a task.

The tasks are then run at `playground/views.py` when a user navigates to the
endpoint.

Note: Did you get the following error after running the task?

```log
[2022-06-04 18:46:07,114: ERROR/MainProcess] Received unregistered task of type 'playground.tasks.notify_customers'.
The message has been ignored and discarded.

Did you remember to import the module containing this task?
Or maybe you're using relative imports?
```

This means a task you created wasn't registered with Celery.

Even though autodiscover is on, Celery may sometimes miss the creation of a new
task. 🙃

To fix this issue you simply need to restart the Celery process.

After restarting, you'll know everything is working if you visit the endpoint
again and your task is displayed in the terminal.

```log
[2022-06-04 18:52:45,353: INFO/MainProcess] Task playground.tasks.notify_customers[556a8b30-9c20-4ad0-96a1-d061be5eb28a] received
[2022-06-04 18:52:45,358: WARNING/ForkPoolWorker-8] Sending 10k emails...
[2022-06-04 18:52:45,359: WARNING/ForkPoolWorker-8] Hello awesome customer!
[2022-06-04 18:52:55,360: WARNING/ForkPoolWorker-8] Emails were successfully sent!
```

### Scheduling Periodic tasks

Celery Beat is used to create a reoccuring task (ie. Send email every Monday at
5pm).

To learn how to schedule periodic tasks, take a look at
`settings.py/CELERY_BEAT_SCHEDULE`.

To run Celery Beat make sure your Django server is up, then run:
`celery -A storefront worker`

Notice that the **'beat'** process is used instead of **'worker'**

You should get something like the following in your terminal

```log
celery beat v5.2.7 (dawn-chorus) is starting.
__    -    ... __   -        _
LocalTime -> 2022-06-04 19:07:17
Configuration ->
    . broker -> redis://localhost:6379/1
    . loader -> celery.loaders.app.AppLoader
    . scheduler -> celery.beat.PersistentScheduler
    . db -> celerybeat-schedule
    . logfile -> [stderr]@%WARNING
    . maxinterval -> 5.00 minutes (300s)
```

### Monitor Celery Tasks with Flower

We can monitor Celery tasks using the Flower library which provides an interactive dashbdoard for reviewing tasks.

To add Flower to your project:
`pipenv install flower`

After installing the library, you can run it with Celery with:
`celery -A storefront flower`

**NOTE:** Make sure your Django server is running!

To view the dashboard open a browser and navigate to `http://localhost:5555`
