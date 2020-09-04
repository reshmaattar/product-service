# Product Service API
## About
This is a simple product service API for CRUD features
## Features
With this API;
- You can create, view, update, and delete a product 
- You can list all products
- You can filter in stock product and sold out product 
  by setting in_stock True or False respectively.
## Technology stack
Tools used during the development of this API are;
- [Django](https://www.djangoproject.com) - a python web framework
- [Django REST Framework](http://www.django-rest-framework.org) - a flexible toolkit to build web APIs
- [Django filter]
- [SQLite](https://www.sqlite.org/) - this is a database server
## Requirements
- Use Python 3.x.x+
- Use Django 2.x.x+
## Running the application
To run this application, clone the repository on your local machine and execute the following command.
```sh
    $ cd to root directory where repo cloned
    $ Install [virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/#installing-virtualenv).
    $ Create a new virtualenv called "venv": `python3 -m venv venv`.
    $ Set the local virtualenv to "venv": `source venv/bin/activate`.
    $ pip3 install -r requirements.txt
    $ python manage.py makemigrations
    $ python manage.py migrate --run-syncdb
    $ python manage.py runserver

    
```
Open localhost:8000/api/products to access api in browser
## Tests

```sh 
    $ python manage.py test
```
## Running the application in docker
To start in container run below command and open localhost:8000/api/products to access api in browser
```sh 
    $ docker-compose -f docker-compose.yml up --build --force-recreate  -d
```

To run test on running container run below command
```sh 
    $ docker exec -it <<container-id>> python manage.py test
```
To stop in container run below command
```sh 
    $ docker-compose -f docker-compose.yml down
```
