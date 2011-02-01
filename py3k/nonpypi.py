# Copyright 2011 Baiju M <baiju.m.mail@gmail.com>. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice, this list of
#       conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright notice, this list
#       of conditions and the following disclaimer in the documentation and/or other materials
#       provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those of the
# authors and should not be interpreted as representing official policies, either expressed
# or implied, of Baiju M <baiju.m.mail@gmail.com>.

from flask import render_template, request, redirect, url_for

from .application import app
from .application import db
from sqlalchemy.exc import IntegrityError

from .model import Distribution
#from .model import User
from .model import Comment
from .utils import get_status, pretty_date


@app.route('/save_new_project', methods=['POST'])
def save_new_project():
    name = request.form['projectname']
    result = Distribution.query.filter_by(name=name).first()
    if result is not None:
        return "A page exist in PyPI"
    import xmlrpclib
    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    if client.package_releases(name):
        try:
            release_data = client.release_data(name, client.package_releases(name)[0])
        except IndexError:
            print name
            return "Cannot create"
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
            return "Cannot create"
        return "A page exist in PyPI" 
    home_page = request.form['home_page']
    author = request.form['author']
    summary = request.form['summary']
    distribution = Distribution()
    distribution.name = name
    distribution.home_page = home_page
    distribution.author = author
    distribution.summary = summary
    distribution.pypi_page = False
    db.session.add(distribution)
    db.session.commit()
    return redirect(url_for('packages_details', name=name))

@app.route('/nonpypi')
def nonpypipkg():
    return render_template('nonpypi_package.html')
