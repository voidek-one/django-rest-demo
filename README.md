# rest-api
Django restful app for storing and sending feedback messages with task queue<br>
git clone 

For sending email you can use google smtp<br>
To run project we need install Python, PostgreSQL and Redis for work with Celery.
<pre>
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib redis-server
</pre>
After, we need create new database and user for postgres.
<pre>
sudo -u postgres psql
postgres=# CREATE DATABASE django_db;
postgres=# CREATE USER django WITH PASSWORD 'password';
postgres=# ALTER ROLE django SET client_encoding TO 'utf8';
postgres=# ALTER ROLE django SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE django SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE django_db TO django;
postgres=# \q
</pre>
We need install python virtual environment, requred libs and configure app settings:
<pre>
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
cd ~/rest-api
python3 -m venv .venv
source /.venv/bin/activate
pip3 install -r requirements.txt
</pre>
open ~/rest-api/settings/settings.py and edit this lines
<code><pre>
SECRET_KEY = '' #input your secret key
EMAIL_HOST_USER = '' #input your gmail
EMAIL_HOST_PASSWORD = '' #input your gmail password
</pre></code>
Next step apply migrations
<pre>
python3 manage.py migrate

</pre>
You can run tests to make sure the app is working
<pre>
python3 manage.py test
</pre>
And start redis to use celery 
<pre>
redis-server
celery worker -A settings
</pre>
Finally run django
<pre>
python3 manage.py runserver
</pre>
API: <br>
For get auth token used djoser <br>
POST      | api/v1/auth/token/login
<pre>
{
"password": "string",
"username": "string"
}</pre>
When database entry created, celery will send email with feedback message.<br>
If need attach files to message specify it **pk** or leave blank if there no files.
<br>
POST|api/v1/feedback
<pre>
{
"full_name": "string",
"email": "user@example.com",
"message": "string",
"files_to_send": [
pk
]
}</pre>
For other CRUD actions, you need create user with superuser permissoins:
<pre>
python3 manage.py createsuperuser
</pre> put auth token in header.<br>
You can upload file it attach to a email message<br>
POST|api/v1/upload
<pre>
content type: multipart/form-data
name = 'uploaded_file' , file_name = 'filename.jpg'
</pre>
Also you can use **swagger** */swagger/* or **redoc** */redoc/* to get more information about API