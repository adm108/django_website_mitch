# django_website_mitch

## Description:

Blog website based on Mitch Tabian's tutorial from youtube:

https://www.youtube.com/playlist?list=PLgCYzUzKIBE_dil025VAJnDjNZHHHR9mW

## Main features:
- registration,
- login and logout,
- creating and updating posts and user profile,
- searching post on main page,
- changing password,
- pagination.

## Technologies:
- Python 3.8,
- Django 3.0,
- HTML 5,
- CSS 3,
- Bootstrap 4,
- JavaScript (small piece of code to make an frontend effect during changin post's pictures).

## Installation:
##### 1. Clone repository:
```sh
$ git clone https://github.com/adm108/django_website_mitch.git
```
##### 2. Create virtual enviroment next to src folder (not inside) and activate it.
##### 3. Install all packages from requirements.txt file:
```sh
$ pip install -r requirements.txt
```

##### 4. Go to src folder and use manage.py to enter following commands. Generate SQL commands:
```sh
$ python manage.py makemigrations
```
##### 5. Execute SQL commands:
```sh
$ python manage.py migrate
```
##### 6. Create superuser (enter email, username and password):
```sh
$ python manage.py createsuperuser
```
##### 7. Inside src folder create folders: "static", "static_cdn", "media", "media_cdn".
##### 8. Put some logo inside static folder and name it: "logocodingwithmitch.png".
##### 9. Collect static files:
```sh
$ python manage.py collectstatic
```
##### 10. Run your local server and have fun:
```sh
$ python manage.py runserver
```
