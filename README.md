#### Our Ubuntu installation first needs system packages for Python development

**We are using python 3.5 for development. Please make sure python 3.5 has installed**

```
sudo apt-get install python3-pip python3-dev virtualenv
```

#### Create a directory to store virtualenvs then put a new virtualenv in it.

Make sure pip and setuptools are the latest versions.

```
pip3 install --upgrade pip setuptools
```

Specify the system python3 installation

```
python3 -m venv <path>/<venv_name>
```
eg: `python3 -m venv ~/venvs/currency_converter`

Activate the virtualenv.

```
source ~/venvs/smartgarden/bin/activate
```

#### Clone the project

```
git clone origin git@github.com:zudheer/currency_converter.git
```
#### Install the required packages

```
pip install -r requirements.txt
```
#### Create local settings

```
cp dotenv.sample .env
```
Edit `settings.py` values as per your local installation. All values are required except Email settings which you may choose to use the defaults.

#### Migrate the database
```
python manage.py migrate
```

#### Create a superuser
```
python manage.py createsuperuser
```


#### Running a locally
```
python manage.py runserver
```
This will run our development server in http://localhost:8000