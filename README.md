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
## Usage

### Authorization
Register using the 'POST' method:
```
POST /register/
{
# required fields
	"email": "user@email.com",
	"username": "Username",
	"password": "password",
# optional fields
	"first_name": "User First Name",
	"last_name": "User Last Name",
# prohibited fields
	"is_staff": false,
	"is_superuser": false
}
```

The endpoint should validate the request body and return a `201 Created` status code with newly created user:
```
{
	"id": 1,
	"last_login": null,
	"is_superuser": false,
	"first_name": "",
	"last_name": "",
	"is_staff": false,
	"is_active": true,
	"date_joined": "2025-11-08T14:42:28.400569Z",
	"username": "Username",
	"email": "user@email.com",
	"groups": [],
	"user_permissions": [],
	"msg": "Registration successful",
	"tokens": {
		"access": "access_token",
		"refresh": "refresh_token"
	}
}
```


After that, login using the 'POST' method:
```
POST /login/
{
	"email": "user@email.com",
	"password": "password"
}
```

The following response with `200 OK` status is expected:
```
{
	"msg": "Login successful. Welcome, User!",
	"tokens": {
		"access": "access_token",
		"refresh": "refresh_token"
	}
}
```


In order to refresh access token, refresh endpoint is used:
```
POST /refresh/
{
	"refresh": "refresh_token"
}
```

This returns `200 OK` status and creates new refresh and access tokens:
```
{
	"access": "new_access_token",
	"refresh": "new_refresh_token"
}
```

### CRUD operations

**For all CRUD operations with posts bearer token is required.**

#### Create a Post
To create a new post, 'POST' method is used:
```
POST /posts/
{
	"title": "My fist Blog Post",
	"content": "This is the content of my first blog post.",
	"category": "Personal",
	"tags": ["One tag", "two tags"]
}
```

The following response with `201 Created` is expected:
```
{
	"id": 1,
	"title": "My fist Blog Post",
	"content": "This is the content of my first blog post.",
	"category": "Personal",
	"tags": [
		"One tag",
		"two tags"
	],
	"author": 1
}
```

#### Read post or posts
To get a single blog post, use 'GET' method and primary key of the post. Alternatively, to get all posts, use 'GET' method alone:
```
GET /posts/{int: pk}
```

The endpoint should return a `200 OK` status code with the blog post(s):
```
[
	{
	"id": 1,
	"title": "My first updated post",
	"content": "This is the updated content of my first post.",
	"category": "Personal",
	"tags": [
		"One tag",
		"two tags"
	],
	"author": 1
	},
	# if you created multiple posts, more will be displayed here
]
```

#### Update a Post
To edit a post, 'PUT' method is used with primary key of a post:
```
PUT /posts/{int: pk}
{
	"title": "My first updated post",
	"content": "This is the updated content of my first post."
}
```

It should return `200 OK` status and display following result:
```
{
	"id": 1,
	"title": "My first updated post",
	"content": "This is the updated content of my first post.",
	"category": "Personal",
	"tags": [
		"One tag",
		"two tags"
	],
	"author": 1
}
```

If needed, category and tags fields can also be updated.

#### Delete a Post
To delete a post, `DELETE` method should be used, as well as primary key of a post:
```
DELETE /posts/{int: pk}
```

It should return `204 NO CONTENT` status and delete a post from database.

### Administration

Users with superuser permissions can perform limited CRUD operations with existing users. To do this, superuser must be created via command line and authorized via bearer token to access '/admin/' endpoint. The following command is used to create a superuser:

```
> python manage.py createsuperuser
```

#### Create a new user
To create a new user, 'POST' method is used. Unlike regular registration, superusers can register new users with superuser and staff permissions.
```
POST /admin/users/
{
	"email": "user@email.com",
	"username": "User",
	"password": "password",
	"is_staff": true,
	"is_superuser": false
}
```

The following response with `201 Created` status is expected:
```
{
	"id": 1,
	"last_login": null,
	"is_superuser": false,
	"first_name": "",
	"last_name": "",
	"is_staff": true,
	"is_active": true,
	"date_joined": "2025-11-08T15:42:59.536518Z",
	"username": "User",
	"email": "user@email.com",
	"groups": [],
	"user_permissions": []
}
```

#### Read all users or specific user
Superuser can use 'GET' method to list all registered users or get information of one user if primary key is specified:
```
GET /admin/users/{int: pk}
```

#### Edit user's information
To edit user's information, 'PATCH' method is used, in addition, primary key of a user is required. Note that even superuser is not authorized to edit personal information, like first name, last name, email, password and username:
```
PATCH /admin/users/{int: pk}
{
	"username": "Another username"
}
```

```
{
	"detail": "You are not allowed to modify the 'username' field."
}
```

However, superuser can give superuser and staff permission to already registered user:
```
PATCH /admin/users/{int: pk}
	"is_superuser": true
}
```

```
{
	"id": 1,
	"last_login": null,
	"is_superuser": true,
	"first_name": "",
	"last_name": "",
	"is_staff": true,
	"is_active": true,
	"date_joined": "2025-11-08T15:42:59.536518Z",
	"username": "User",
	"email": "user@email.com",
	"groups": [],
	"user_permissions": []
}
```

#### Deleting the user
Superuser can delete another user's profile, even if user to be deleted has superuser permissions: 
```
DELETE /admin/users/
```

This will return `204 No Content` status and user will be deleted from database, as well as all of the posts he created by cascade deletion.

However, to prevent errors, superuser cannot delete its own account:
```
DELETE /admin/users/
```

```
{
	"detail": "You cannot delete your own superuser account."
}
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
