# backend
Everything Backend 

Create a virtualenv
```
virtualenv [ your env name ]
```
Create .env file in backend folder with the following fields. Replace the value according to your environment.

```env
DATABASE=postgres
DB_USER=db_user_name
DB_PASSWORD=db_password
HOST_ADDRESS=localhost:5432
DB_NAME=db_name
```
Install Packages
```
pip install -r requirements.txt
```
Create DB (Postgres)
```
createdb db_name
```
**Development Server**
```bash
export FLASK_APP=server
export FLASK_ENV=development

# run migrations once
flask db upgrade

flask run
```

## API Documentation
Pending!