from py3k.model import Distribution
import xmlrpclib
client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')

# XXX: Remove these hard-coding later
package_names = ['zope.interface', 'Twisted']
#package_names = client.list_packages()

for name in package_names:
    release_data = client.release_data(name, client.package_releases(name)[0])
    home_page = release_data['home_page']
    author = release_data['author']
    summary = release_data['summary']
