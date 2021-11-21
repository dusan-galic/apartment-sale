import eventlet
eventlet.monkey_patch()

from runner import create_flask_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from core import db, socketio
from manager_commands import create_admin_user


app = create_flask_app()
migrate = Migrate(app, db)
manager = Manager(app)
server = Server(host="0.0.0.0", port=7777)

# command for running app: python prodajastanova.py runserver
# socketio.run(app, host='0.0.0.0', port=7777, use_reloader=False)
manager.add_command('runserver', socketio.run(app, host='0.0.0.0', port=7777, use_reloader=False))
# command for migrates
manager.add_command('db', MigrateCommand)
# command for creating admin user
manager.add_command('create_admin_user', create_admin_user.CreateAdminUser())

if __name__ == '__main__':
    manager.run()
