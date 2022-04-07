# Project for QA Winter 2021

## Application theme
The application is an asset managing application that allows a user to register an account, manage, and unassign their assets along with having a standard
user privileges and admin user privileges.

## The frontend 
The frontend is heavy based on the [NHSUK frontend](https://github.com/nhsuk/nhsuk-frontend)
Also following guidance from [NHS Digital Service Manual](https://service-manual.nhs.uk/)

## Tech stack
- [Python 3.9](https://docs.python.org/3/)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [Heroku](https://devcenter.heroku.com/)
- [Postgres](https://www.postgresql.org/docs/)

## Deployment
- [Gunicorn](https://gunicorn.org/)
- [Heroku deployed app](https://uni-nhs-asset-manager.herokuapp.com/login)

## users

### Admin user
- Email: admin@user.com
- Password: testing123
### standard user
- Email: standard@user.com
- Password: testing123

Also feel free to create your own standard user.

### Dummy users
- Generated using [Mockaroo](https://www.mockaroo.com/)
- Within the application you will find an array of dummy users these accounts can't be logged into as they're there for testing purpose only. The main reason these accounts can't be logged into is because of the pbkdf2_sha256 password verification, because the data has been imported into the database these users passwords have not been hashed, therefore are inaccessible.

## Steps to installing requirements and running the project locally
- Open terminal
- ``` cd nhs-asset-manager ``` to the directory
- ``` virtualenv env ``` to create a virtual environments
- ``` . env/bin/activate ``` to activate the virtual env
- ``` pip install -r requirements.txt ``` to install the included requirements
- ``` python app.py ``` will run the application
- ``` 127.0.0.1:5000 ``` use this url to view the project in your browser

## DB connection 
You will need to attach your own Postgres to the os variable.
- Open terminal
- ```export DATABASE=YOUR DATABASE STRING```
- You will need to uncomment the create database inside ```models.py``` to automatically create the db and tables

## Testing
- pytest 
- run tests using ```pytest``` in the base directory



