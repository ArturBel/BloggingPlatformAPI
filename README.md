# BloggingPlatformAPI

## Description
Simple REST API with basic CRUD operations for a personal blogging platform built with Django Framework. Project was inspired by [Blogging Platform API](https://roadmap.sh/projects/blogging-platform-api) by roadmap.sh.

---
## Project structure
```
BloggingPlatformAPI/
├── api/
│   ├── migrations/         # migration files
│   ├── tests/              # directory with test scripts
|   |   ├── test_admin.py   # script to test admin endpoint
|   |   ├── test_auth.py    # script to test login and registration
|   |   ├── test_crud.py    # script to test crud operations
|   ├── __init__.py
|   ├── admin.py            # admin configuration and registration
│   ├── apps.py             # app configuration
│   ├── auth.py             # authorization views
│   ├── models.py           # app's models
|   ├── posts_crud.py       # crud/posting views
|   ├── serializers.py      # serializers for models
|   ├── superuser.py        # superuser view
|   ├── urls.py             # app's urls registration
├── bloggingplatform/
|   ├── __init__.py
|   ├── asgi.py             # asgi configuration
|   ├── settings.py         # settings of project
|   ├── urls.py             # project's urls registration
|   ├── wsgi.py             # wsgi configuration
├── .env                    # secrets are stored here
├── .env.example            # example of how .env should look like
├── .gitignore              # ignored files
├── manage.py               # command line utility
├── requirements.txt        # project requirements
└── README.md               # readme file
```

---
## Main features
- Multiple users registration
- Authorization via JWT tokens
- Refresh tokens for JWT renewal
- CRUD operations for blog posts
- Test scripts for scalability
---
## Installation
1) Clone the repository:
```
> git clone https://github.com/ArturBel/BloggingPlatformAPI.git
> cd BloggingPlatformAPI
```

2) Create and activate virtual environment:
```
> python -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
```

3) Create database in Postgres for storage and apply migration.
```
psql> CREATE DATABASE bloggingplatformapi OWNER postgres;
> python -m manage.py migrate                           
```

4) Create .env file to store secrets, paste there example file and add real values:
```
SECRET_KEY=django-secret-change-it
DEBUG=False
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_NAME=database
DATABASE_HOST=localhost
DATABASE_PORT=5432
ADMIN_EMAIL=admin@email.com
ADMIN_PASSWORD=admin_password
```

4) Run:
```
> python manage.py runserver
```

---
## Testing

To test all functions of BloggingPlatformAPI, including registration, login and CRUD, run the following command:
```
> python manage.py test
```

---
## Author

Artur Belotserkovskiy
- Github: https://github.com/ArturBel
