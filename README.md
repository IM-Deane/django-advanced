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

### Managing Redis Cache Content

We can use the Redis CLI to manage cached content.

First we need to find the ID of our Redis container: `docker ps`

Your terminal should then show a list of Docker containers. Find the image named
'redis' and copy its container ID.

```log
CONTAINER ID   IMAGE       COMMAND
96ecae9c8c35   redis       "docker-entrypoint.s…"
```

After that you can run the following command to launch the Redis CLI:
`docker exec -it <redis-container-id>`

This should start the redis CLI where you can then select the database number
(we used 2 for django-redis setup) and the `keys *` command to view the
currently cached keys.

Example:

```log
127.0.0.1:6379> select 2
OK
127.0.0.1:6379[2]> keys *
(empty array)
127.0.0.1:6379[2]>
```

**NOTE:** If your cache is empty like above, its because it expired. To refresh
the cache, open a client and navigate to any of the playground endpoints.

Example: `http://localhost:8000/playground/hey/`

Remember that the first request will call the API and then cache the data! So
you'll need to refresh the page to verify that your cache is working.

Once you have some cached data, you can navigate back to the Redis CLI and run
`keys *` again.

You should now have a list of cached data like below.

```log
127.0.0.1:6379[2]> keys *
1) ":1:views.decorators.cache.cache_header..1c82a80318e179b87c2754ee558252b0.en-us.UTC"
2) ":1:views.decorators.cache.cache_page..GET.1c82a80318e179b87c2754ee558252b0.d41d8cd98f00b204e9800998ecf8427e.en-us.UTC"
```

### Cache commands

To select the Redis database: `select <database-id>`

To view all currently cached keys: `keys *`

To delete a specific key you can run: `del <cache-key>`

To clear the entire cache you can use: `flushall`
