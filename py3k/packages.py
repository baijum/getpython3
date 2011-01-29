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
#from flask import session
from .model import Distribution
#from .model import User
from .model import Comment

from .application import app
from .application import db

@app.route('/package/+<int:page_number>')
def packages_browse_page(page_number):
    result = Distribution.query.all()
    return render_template('show_package.html', result=result)

@app.route('/package/<name>/add_comment', methods=['POST'])
def add_comment(name):
    fullname = request.form['fullname']
    email = request.form['email']
    working = request.form['comment[works_for_me]']
    platform = request.form['comment[machine_platform_id]']
    comment = request.form['comment[body]']
    new_comment = Comment()
    result = Distribution.query.filter_by(name=name).first()
    new_comment.distribution_id = result.id
    new_comment.fullname = fullname
    new_comment.email = email
    new_comment.working = True if working == 'true' else False
    new_comment.platform = platform
    new_comment.comment = comment
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('packages_details', name=name))


@app.route('/package/<name>')
def packages_details(name):
    result = Distribution.query.filter_by(name=name).first()
    return render_template('package_details.html', result=result)


@app.route('/package', methods=['GET', 'POST'])
def packages():
    if request.method == 'POST':
        return redirect(url_for('packages_details', name=request.form['pkgname']))
    else:
        return redirect(url_for('packages_browse_page', page_number=1))
