# ECM2434
Breadscrums
---
# Running the project
The backend is run from the src/ directory, so before running any commands you should ensure that your terminal is in that directory

To setup the database, which will be needed if you have freshly cloned the project, run:
`python manage.py migrate`

To run the server, simply run:
`python manage.py runserver`

If you are using the admin site, then you may want to first create a superuser:
`python manage.py createsuperuser`

If your IDE is marking imports as errors, then you can go into settings (pylint settings for me) and add "./src" to source path

# Dependencies
All dependencies needed are a part of the settings.py file which is located in src/ecoGo. These are automatically installed when running the server. 

# Testing basic functionalities
There are two ways to test our project's functionalities. Using the unit tests written, and by performing manual tests.

Regarding the login system, all unit tests are within the src/apps/user, located in tests.py. You can run these tests using the command `python manage.py test apps/user` while being in the project directory. This should run the tests through your terminal. Secondly, you can test the system by runnning the server and performing manual tests to ensure that login, register operations work as intended. 
