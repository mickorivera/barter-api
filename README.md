# irithm-cards
Sample Flask Rebar App


## Requirements
Tested on Python 3.6.5
Expected to work on Python >3.6

## Environment Setup
### Creation and Activation of Virtual Environment
```bash
pip install virtualenv
virtualenv --python=python3.6 venv
source venv/bin/activate
```
### Installation of Libraries
```bash
pip install -r requirements
```

### Database Creation
Requirement: Postgresql
```bash
service postgresql start
service postgresql status
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';"
sudo -u postgres createdb irithm
```

### Schema Migration
Run peewee-migrate cli
```bash
pem migrate
```

### Initial Data Seed
```bash
python seed.py
```

### Unit Tests
```bash
 pytest -vv tests --cov-branch --cov=app
```

### Run Application
```bash
python manage.py
```

Locally, you can access the Swagger Documentation [here](http://127.0.0.1:5000/v1/swagger/ui)
