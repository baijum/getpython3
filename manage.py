# manage.py

from flaskext.script import Manager

from py3k.application import app

manager = Manager(app)

@manager.command
def hello():
    print "hello"

if __name__ == "__main__":
    manager.run()
