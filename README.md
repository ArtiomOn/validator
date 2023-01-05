# VALIDATOR

## Requirements
1. Python 3.10 or higher

# .env file
```python
# DJANGO
SECRET_KEY=
DEBUG=True
```

## Commands
```shell
python manage.py update_domains
```

#### Run tests
```shell
python manage.py test
```

#### Deployment
``` shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
