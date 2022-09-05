# Notification service app

The application is implemented:

   - Adding a new client to the directory with all its attributes
   - Updates to client attribute data
   - Deleting a client from the directory
   - Adding a new mailing list with all its attributes
   - Getting general statistics on created mailings and the number of messages sent on them, grouped by status
   - Getting detailed statistics of sent messages on a specific mailing list
   - Mailing list attribute updates
   - Mailing list deletions
   - Processing active mailings and sending messages to clients

Stack: Celery, Django, Django Rest Framework, PostgresSQL, Redis

## Install:

   - git@github.com:ieasycat/notification_service_app.git  
   - virtualenv -p python3 .venv
   - source venv_name/bin/activate
   - python -m pip install -r requirements.txt
   - Creation .env file. Example .env_example

## Starting migrations and filling the database with data:

   - python manage.py makemigrations
   - python manage.py migrate
   - python manage.py loaddata main_fixtures.json
   
## Creating a superuser:

   - python manage.py createsuperuser
   
## Launching the application:

   - python manage.py runserver
   
## Launching the celery:

   - celery -A notification_service worker -l info
   - celery -A notification_service flower --port=5555

```
http://127.0.0.1:5555 Flower
```

## Docker:

   - Creation .env_docker file. Example .env_docker_example
   - docker-compose up -d --build

## Description of methods and documentation:

```
http://127.0.0.1:8000/docs/
```

## Running tests:
  - pytest
  - View % code coverage

````
   pytest --cov=.
````

## Technical task:
To design and develop a service that, according to the specified rules, launches a mailing list of clients.
   
The "mailing list" entity has the attributes:
   
   - Unique mailing id
   - Date and time of the newsletter launch
   - Text of the message to be delivered to the client
   - Filter the properties of the clients on which the mailing should be made (mobile operator code, tag)
   - Date and time of the end of the mailing list: if for some reason they did not have time to send out all the messages, no messages should be delivered to               customers after this time
   
The "client" entity has the following attributes:

   - Unique client id
   - Client phone number in 7XXXXXXXXXX format (X is a digit from 0 to 9)
   - Mobile operator code
   - Tag (arbitrary label)
   - Time zone

The "message" entity has the following attributes:

   - Unique message id
   - Date and time of creation (sending)
   - Sending status
   - Id of the mailing list within which the message was sent
   - Id of the client to whom the message was sent
   
Design and implement an API for:

   - Adding a new client to the directory with all it's attributes
   - Updating client attribute data
   - Removing a client from the directory
   - Adding a new mailing with all it's attributes
   - Getting general statistics on created mailings and the number of messages sent on them with grouping by statuses
   - Getting detailed statistics of messages sent on a specific mailing list 
   - Updating mailing list attributes
   - Deleting mailing lists
   - Processing active mailings and sending messages to clients

### Additional tasks:

  - Testing the code, 87% (item №1)
  - Prepare docker-compose to run all project services with one command (item №3)
  - Documentation (item №5)
  - Admin Web UI - 'http://127.0.0.1:8000/admin/' (item №6)
  - Processing remote server errors and creating the status of an 'Error' message, followed by the creation of a periodic task (item №9)
  - An additional possibility of sending notifications to clients depending on the client's time zone has been implemented. If the time does not match the    required range, the task gets the status 'Wrong Time' and will be restarted after 1 hour (item №11)
