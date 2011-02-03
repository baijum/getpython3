import sys
from py3k.application import db
from py3k.model import Distribution
from sqlalchemy.exc import IntegrityError
import xmlrpclib
client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')

package_names = client.list_packages()
result = db.session.query(Distribution).all()
existing_package_names = set([p.name for p in result])
package_names = set(package_names)
diff_package_names = existing_package_names ^ package_names

demo = False
count = 0
try:
    demo = sys.argv[1]
    if demo == "--demo":
        demo = True
except KeyError:
    pass

for name in diff_package_names:
    if demo and count > 100:
        break
    count = count + 1
    try:
        release_data = client.release_data(name, client.package_releases(name)[0])
    except IndexError:
        print name
        continue
    home_page = release_data['home_page']
    author = release_data['author']
    summary = release_data['summary']
    distribution = Distribution()
    distribution.name = name
    distribution.home_page = home_page
    distribution.author = author
    distribution.summary = summary
    distribution.pypi_page = True
    db.session.add(distribution)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

