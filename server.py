from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from app.db.schema import setup_db
from flask_script import Manager

from app.auth.routes import auth
from app.student.routes import student


app = Flask(__name__)
setup_db(app)
app.register_blueprint(auth)
app.register_blueprint(student)
@app.route('/')

def hello_world():
	return 'YOYO'

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    app.run()
