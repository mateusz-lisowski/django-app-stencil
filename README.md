# Django test deploy app

Django test app for checking CI/CD pipelines and integration with servers.
It is a skeleton project for integrating all common libraries and making your code easy-to-start.

## Project structure
- **Django** as the main backbone of the project
- **Postgres** as the main database
- **Redis** as the caching database
- **Docker** as the main deployment engine
- **Jenkins** as CI/CD solution

### Django app dependencies
- **Gmail** as mailing service (just for starting)
- **whitenoise** as staticfiles-serving library (just for starting)
- **python-decouple** for managing .env files
- **django-allauth** for out-of-the-box authentication
- **django-allauth-ui** for making allauth look good
- **gunicorn** for serving django app as wsgi

## Helpful commands

### Check if django is deploy-ready
```commandline
python manage.py check --deploy
```

### Lint project with flake8
```commandline
flake8 --max-line-length 120
```

### Test chosen app
```commandline
coverage run --source='.' manage.py test myapp
```

### Test whole project
```commandline
coverage run --source='.' manage.py test .
```

### Get a coverage report
```commandline
coverage report
```