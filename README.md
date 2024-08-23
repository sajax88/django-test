## Test Django + DRF project for Sightline
- Python: 3.12
- PostgreSQL: 16.4 

Run `docker-compose up` to build and start the application.

Run `./manage.py loaddata sales.json` to load some test data into the db.

### A couple of thoughts about the models
- "category" field is a nullable Char that is not usually recommended for Django. I guess in real world it could be a nullable FK field. I kept a default blank string according to Django doc.
- I would rename "date_of_sale" field since it's really a datetime field and the name can be misleading.

### Authentication and security considerations

- Setup HTTPS-only connection
- Setup [CORS headers](https://pypi.org/project/django-cors-headers/)
- Require user authentication since we probably don't want to share our statistics. 
For example, we can use DRF TokenAuthentication, they also recommend using
[Knox](https://github.com/jazzband/django-rest-knox) or [JWT](https://pypi.org/project/djangorestframework-simplejwt/).
- Check out [Django checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/) before deploy.

### Optimization and efficiency considerations

- We could think about limiting the data for the chart endpoint by default (e.g. displaying just last year), so getting all the data would not be a default option. Maybe even make the date filters required.
- Since the sales records are not likely to change, we could cache the aggregated results (need to add dates range to the cache key).
- We can use a profiler to monitor the requests time and decide if anything requires optimization
(I've used [Silk](https://github.com/jazzband/django-silk), but of course there are many of them). 
Sentry also has some performance monitoring and even looks for N+1 problems, among other things.


### Other considerations
- We're dealing with money, so rounding question (for average price) should be discussed with business
- SalesAggregationFilter duplicates SalesListFilter, but it's probably better to keep them separate if they are not linked in UI.
- I have not added the date filters validation (end_date >= start_date, no future dates), because in the worst case they just won't get any data, but we could add them for better user experience and to avoid unnecessary calls to db.
- Thanks for reminding me how much I hate Django aggregations :)
