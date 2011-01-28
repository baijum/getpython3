from py3k.application import db
from py3k.model import Distribution
import xmlrpclib
client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')

# XXX: Remove these hard-coding later
package_names = ['zope.interface',
                 'Twisted',
                 'treedict',
                 'sqlite3dbm',
                 'splinter',
                 'slacklog',
                 'etm',
                 'lcnester',
                 'askbot',
                 'runFBTests',
                 'selenium-saucelabs-python',
                 'translitcodec',
                 'etsy',
                 'm2wsgi',
                 'pybedtools',
                 'Cobaya',
                 'podcaster',
                 'isotoma.recipe.cluster',
                 'mcweb',
                 'isotoma.zope.testpythonscript',]
#package_names = client.list_packages()

for name in package_names:
    release_data = client.release_data(name, client.package_releases(name)[0])
    home_page = release_data['home_page']
    author = release_data['author']
    summary = release_data['summary']
    distribution = Distribution()
    distribution.name = name
    distribution.home_page = home_page
    distribution.author = author
    distribution.summary = summary
    db.session.add(distribution)

db.session.commit()
