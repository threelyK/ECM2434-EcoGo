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