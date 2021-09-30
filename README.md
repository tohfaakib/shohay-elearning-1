**Clone The Project**

`git clone https://github.com/shohay/shohay-elearning.git`

**Get into the project directory, create virtual env and activate it**

**Install Requirements**

`pip install -r requirements.txt`

**Migrate the tables**

`python manage.py makemigrations`

`python manage.py migrate`

**Migrate the specific table**

`python manage.py makemigrations <app_name>`

`python manage.py migrate <app_name>`

**Create superuser**

`python manage.py createsuperuser`

**Start the server**

`python manage.py runserver`

**Open `http://127.0.0.1:8000/admin` and login to the admin dashboard the username and password you created in the previous step.**
