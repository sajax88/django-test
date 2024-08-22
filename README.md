## Test Django + DRF project for Sightline
- Python: 3.12
- PostgreSQL: 16.4 
- Redis: 7.4

Run `docker-compose up` to build and start the application.

Run `./manage.py loaddata sales.json` to load some test data into the db.

### Authentication and security considerations

- Setup HTTPS-only connection
- Setup [CORS headers](https://pypi.org/project/django-cors-headers/)
- Require user authentication since we probably don't want to share our statistics. 
For example, we can use DRF TokenAuthentication, they also recommend using
[Knox](https://github.com/jazzband/django-rest-knox) or [JWT](https://pypi.org/project/djangorestframework-simplejwt/).
- Check out [Django checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)

### Optimization and efficiency considerations

- We can use a profiler to monitor the requests time and decide if anything requires optimization
(I've used [Silk](https://github.com/jazzband/django-silk), but of course there are many of them)
- Sentry also has some performance monitoring and even looks for N+1 problems, among other things.

### A couple of thoughts about the models
- "category" field is a nullable Char that is not usually recommended for Django. I guess in real world it could be a nullable FK field. I kept a default blank string according to Django recommendations for now.
- I would rename "date_of_sale" field since it's really a datetime field and the name can be misleading.

### Other considerations
