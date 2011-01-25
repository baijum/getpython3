import sys
sys.path.append('/home/py3k/getpython3/')
activate_this = '/home/py3k/getpython3/ve/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
from py3k.application import app as application
