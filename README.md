# Caching

## Description

This project was created while following
[codewithmosh.com's](https://codewithmosh.com/p/the-ultimate-django-series)
Ultimate Django Series.

In part 3, we learn about advanced concepts regarding Django utilities.

This branch contains the section on data caching with
[Redis](https://redis.io/docs/getting-started/)

The purpose of this repo is to act as reference when implementing it future
projects.

### What is Caching

Caching is a technique for boosting the performance of your application.

If you find that you're repeatedly fetching the same data from a database, you
can store the response in memory.

Then, the next time you need that data, you can choose to grab it from memory
instead of hitting the database again.

Caching is best used with data that doesn't change very often.

Another usecase, is when dealing with very slow and complex requests. Caching
the response from these types of queries can help mitgate the strain the put on
your app.

### Warning

You should be careful when deciding what data to cache. If used improperly, this
techinque can actually slowdown your project.

As Donald Knuth says:

> Premature optimization is the root of all **evil**.

## Cache Backends in Django

Django comes with several caching backends:

- Local memory (default and best for development)
- Memcached
- Redis
- Database
- File system

In this project we'll be using Redis as its easy to setup and because we also
used it in the section on Celery.

### Django-Redis

We're using the [django-redis](https://github.com/jazzband/django-redis) library
to cache data in Django.

Take a look at the `CACHES` config in settings.py for details on how to add it
Django.

### Using Redis Caching in Django

Take a look at `playground/views.py` for several different examples on how to
cache data.
