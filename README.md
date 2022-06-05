# Advanced Django Concepts

This project was created while following part 3 of
[codewithmosh.com's](https://codewithmosh.com/p/the-ultimate-django-series)
Ultimate Django Series.

In the final part of the series, we learn about advanced concepts in Django.

This branch contains a reference for how to prepare your Django application for
production.

### Static Assets

When you're ready to deploy your application, you'll need to update your static
asset configuration.

First, ensure your `STATIC_ROOT` is configured in `settings.py`.

Then you can collect your projects static assets using:

```python
python manage.py collectstatic
```

If successful, you should see something like:

```log
137 static files copied to '<PATH_TO_PROJECT>/django-advanced/static'.
```

**Note:**

During development (ie. Debug=True) Django automatically collects and servers
your site's static files.

However, during production this is not the case so we need to run the above
command before deploying.

### Serving Static Files

Django doesn't serve static files in production. There are various libraries to
accomplish this, but this project will be using
[whitenoise](http://whitenoise.evans.io/en/stable/).

This library is much simpler to setup compared to alternatives like AWS S3
buckets.

### Logging

Adding a logger is important for addressing any errors that appear when your app
is running in production.

Take a look at this project's `LOGGING` variable in `settings.py` to learn how
to set it up.

This project is configured to use console and file loggers. Again, please look
at the settings.py variable for implementation details.

To learn how to use a logger in your project, take a look at
`playground/views.py`

### Managing Development and Production Settings

Its imperativate to properly manage your projects environment settings.

At a basic level, you should have different configurations for development vs
production.

**Warning:** Not all tutorials mentioned this when I was starting out, but you
should never store your passwords or other sensitive data in your project files
(ie. settings.py)!

Make sure you keep this type of information in an .env variable or else you
**will** regret it.

Take a look at the .env.example file for this projects .env variables.

There are many different ways (and opinions) on how to configure your
envinroments.

This project uses a settings folder approach with separate files for each
environment.

However, i've worked with companies that keep everything in `settings.py` and
use .env variables and conditional statements to determine which settings to
use.

I'd try out different approaches and see which you prefer.

### Serving the project with Gunicorn

During development Django uses a built-in server for running our application.

In production we need something more robust which is where Gunicorn (ie.
Green-Unicorn) comes in.

To add it to our project use: `pipenv install gunicorn`

To serve our app: `gunicorn storefront.wsgi`

This command spins up a gunicorn server and uses the wsgi file as an entry
point.

If the command was successful you should see something similar in your terminal:

```log
[2022-06-04 18:56:53 -0600] [93817] [INFO] Starting gunicorn 20.1.0
[2022-06-04 18:56:53 -0600] [93817] [INFO] Listening at: http://127.0.0.1:8000 (93817)
[2022-06-04 18:56:53 -0600] [93817] [INFO] Using worker: sync
[2022-06-04 18:56:53 -0600] [93818] [INFO] Booting worker with pid: 93818
```

**Note**

Gunicorn is much faster than the Django server but doesn't register file
changes.

Thus it's really only suited for production.
