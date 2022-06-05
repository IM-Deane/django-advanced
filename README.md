# Production & Deployment

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

## Deployment

Django applications can be hosted using:

- Virtual Private Servers (VPS)
- Platform-as-a-Service (PaaS)

Generally, VPSs are cheaper but are much more complex to setup and maintain.
Therefore, unless you have solid DevOps experience its best to stick to PaaS.

Some well known PaaS inlcude:

- Heroku
- Digital Ocean
- MS Azure
- Google Cloud

This project uses Heroku as its very easy to use and hides alot of complexity.

### Setting up Heroku

To complete this section, you'll need a valid Heroku account (don't worry its
free).

If you don't have one, you can sign up here: https://signup.heroku.com/

You'll also need to download the Heroku CLI tool to deploy your project.

If you need to download it, you can do so here:
https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli

**Login** Once you have an account, open a terminal in the root of this project
and run: `heroku login`

This will start the login process where you can then sign into your account.

If successful, you'll see a message in the terminal with your account:

```log
Logging in... done
Logged in as tristandeane93@gmail.com
```

**Create a Heroku App**

Next we need to create a Heroku app which will give us everything we need to
host our project.

To create an app run: `heroku create <APP_NAME>`

Success looks like:

```log
heroku create djangotut-prod
Creating ⬢ djangotut-prod... done
https://djangotut-prod.herokuapp.com/ | https://git.heroku.com/djangotut-prod.git
```

After creating the app, you need to add the new domain to the ALLOWED_HOSTS list
in `settings/prod.py`.

```python
# storefront/settings.py

ALLOWED_HOSTS = ['your-app-name.herokuapp.com']
```

**Note**

Ensure the address doesn't contain 'https://' or any trailing slash after
'.com'.

### Setting Environment Variables

In our production file we are using .env variables. Heroku will need access to
these for our app to run.

But first, you need to generate a SECRET_KEY for your app.

For this project, I used https://djecrety.ir/ which is secret key generator for
Django.

If you used the above site, the key is generated and then copied to your
clipboard.

From here you need to run the following command in your terminal:

```log
heroku config:set SECRET_KEY="<PASTE_YOUR_SECRET_KEY>"
```

Once that's complete the key is copied to Heroku and your site is now a little
more secure.

Before you start celebrating, we need to add another environment variable.

This time we're updating the `storefront/wsgi.py` file and specifying our Heroku
app as the entry point.

In the terminal run the following:

```log
heroku config:set DJANGO_SETTINGS_MODULE=storefront.settings.prod
```

That's it for our environment varibles!

Next we need to create a Procfile which Heroku uses to start our app.

### Creating a Procfile

A Procfile (ie. Process File) let's Heroku know how to launch our project.

This file contains three commands for running application:

```
release: python manage.py migrate
web: gunicorn storefront.wsgi
worker: celery -A storefront worker
```

There's nothing magical going on here. The release process will automatically
run any database migrations.

The web process starts a gunicorn server.

The worker process creates a celery instance that watches our project for async
tasks.

### Setting up a Database

To provision a production database for your app you'll need to use your apps
dashboard in Heroku.

https://dashboard.heroku.com/apps/

For this project we're using PostgreSQL.

So in your apps dashboard, navigate to the "Add-ons" section which can be found
in the "Resources" tab.

In the input field, enter "postgres" and you'll be given several options to
choose from.

I usually opt for "Heroku Postgres" as its simple to setup and has a free-tier.

You can find more about this plugin here:
https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres

For the sake of this tutorial i'm going to assume you went with "Heroku
Postgres".

Once you've completed the add-on process, you should now have Postgres database
connected to your project.

We can confirm this by running the following command in our terminal:
`heroku config`

This command list's all of our projects environment variables.

After running the above command you should see a new `DATABASE_URL` in the list.

```log
=== djangotut-prod Config Vars
DATABASE_URL:           postgres://mvaaopewlclooc:44489cef034e52489c1bed91d551d2f7832dda4c84a970de2a042c706d751310@ec2-54-147-33-38.compute-1.amazonaws.com:5432/df41ltnq1h2k6p
DJANGO_SETTINGS_MODULE: storefront.settings.prod
SECRET_KEY:             <YOUR_SECRET_KEY>
```

This variable was added to your project by the Heroku Postgres add-on.

**Connecting to the Production DB** For the final step in the process, we need
to connect our app to the Heroku database we just created.

For the sake of simplicity, we'll use the
[dj-database-url](https://github.com/kennethreitz/dj-database-url) library to
parse our DATABASE_URL variable.

Install the package by running:

`pipenv install dj-database-url`

Next, open your project's `storefront/settings/prod.py` file and add the
following:

```python
import dj_database_url
...

DATABASES = {
    'default': dj_database_url.config()
}
```

The `dj_database_url.config()` function will check the current environment for
the `DATABASE_URL` variable and parse the connection string for the values
needed to connect to the database.

Easy peasy.

### Adding a Redis instance

Provisioning a Redis instance on Heroku is very similar to setting up a
database.

Navigate to your application's dashboard and find the Add-on section in the
Resources tab.

Search for Redis in the input field and then select Heroku Redis.

You can find more details about this add-on here:

https://devcenter.heroku.com/articles/heroku-redis#provisioning-the-add-on

**Note** Provisioning Redis can take a little longer than creating a database so
be patient.

Once the process is complete we can check our project's variables:

`heroku config`

The output should look similar to this:

```log
=== djangotut-prod Config Vars
DATABASE_URL:           postgres://mvaaopewlclooc:44489cef034e52489c1bed91d551d2f7832dda4c84a970de2a042c706d751310@ec2-54-147-33-38.compute-1.amazonaws.com:5432/df41ltnq1h2k6p
DJANGO_SETTINGS_MODULE: storefront.settings.prod
REDIS_TLS_URL:          rediss://:p5436cb51bfb2d9f014a6d5b21e5919aa8037c4ad16695be15e4eebf485556711@ec2-50-17-230-60.compute-1.amazonaws.com:27200
REDIS_URL:              redis://:p5436cb51bfb2d9f014a6d5b21e5919aa8037c4ad16695be15e4eebf485556711@ec2-50-17-230-60.compute-1.amazonaws.com:27199
SECRET_KEY:             <YOUR_SECRET_KEY>
```

You should now have two more variables in the output: `REDIS_URL` and
`REDIS_TLS_URL`

In the project we're using Redis as both a message broker for Celery and a
Caching system.

So we'll need to add the `REDIS_URL` to the Celery and Cache configs found in
`storefront/settings/prod.py`.

First we need to grab the Redis connection from our environment:

```python
REDIS_URL = os.environ['REDIS_URL']
```

Then we can add the URL to Celery and the Cache:

```python
CELERY_BROKER_URL = REDIS_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 10 * 60, # 10 minutes
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

Congratulations, your project now has a production ready Redis instance!

### Setting up an SMTP Server

There are a lot of options on Heroku for mail servers but right now i'm liking
[Mailgun](https://elements.heroku.com/addons/mailgun)

We can add it to our project by navigating to the Add-on section in the
Resources tab of your app's Heroku dashboard.

Search for **Mailgun** and follow the signup process (it has a free-tier).

Once that's complete, run:

`heroku config`

You should have a bunch of new variables in your terminal:

```log
=== djangotut-prod Config Vars
...
MAILGUN_API_KEY:        cb75321f8c265dd98d08e5ad7804f014-27a562f9-4e042434
MAILGUN_DOMAIN:         sandboxe1799cc713014c9a878737bd52bcf4c4.mailgun.org
MAILGUN_PUBLIC_KEY:     pubkey-4cb9c752a0712d0bd9eb03aba288bfdb
MAILGUN_SMTP_LOGIN:     postmaster@sandboxe1799cc713014c9a878737bd52bcf4c4.mailgun.org
MAILGUN_SMTP_PASSWORD:  d6f53dc188d44be065cb7c6b1e6daece-27a562f9-a34558f0
MAILGUN_SMTP_PORT:      587
MAILGUN_SMTP_SERVER:    smtp.mailgun.org
...
```

We'll need to add these variables to our Email config found in
`storefront/settings/prod.py` look so:

```python
EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
```

After updating the settings, you now have a scalable production SMTP server!

### Deploying our App

Once you've provisioned the necessary add-ons for your project its time to ship
your application.
