Test Django
============

This project is a test in Django. The application allows importing the Trello data for a user.

It has the following cases of use.

- Login with OAuth in Trello.
- Homepage to see the boards loaded for the authenticated user.
- An action to load the data from Trello.

Install
-------

The project uses Docker and you need to create the containers. To do that go to the folder ".devcontainer"
and run "docker-compose up".

If you prefer you can use "vscode" with the "Remote containers" extension and open the project from it.

Run
---

Once the project is opened inside the container you need enter in and run this command "python manage.py runserver_plus 0.0.0.0:8000"

The container maps the port 8000 to 8001 for this reason you need to open the application in this URL:

http://localhost:8001/

Testing
-------

To run the tests you may run this command "pytest".
