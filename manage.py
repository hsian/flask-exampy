
import os

from app import create_app, db
from app.models import User, Role, Permission
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand


app = create_app('production')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role,
                Permission=Permission)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host = '0.0.0.0'))

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models import Role, User

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

    # create users
    User.insert_users()

    # create admin
    User.insert_admin()

if __name__ == '__main__':
	manager.run()