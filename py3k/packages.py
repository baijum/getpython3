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

import datetime

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
    working = request.form['working']
    platform = request.form['platform']
    version = request.form['version']
    comment = request.form['comment[body]']
    new_comment = Comment()
    result = Distribution.query.filter_by(name=name).first()
    new_comment.distribution_id = result.id
    new_comment.fullname = fullname
    new_comment.email = email
    new_comment.working = True if working == 'true' else False
    new_comment.platform = platform
    new_comment.version = version
    new_comment.comment = comment
    new_comment.datetime = datetime.datetime.now()
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('packages_details', name=name))


def get_status(working):
    if working is True:
        working_status = 'works'
        working_status_text = 'Working'
    else:
        working_status = 'fails'
        working_status_text = 'Failing'
    return working_status, working_status_text


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    Source: http://stackoverflow.com/questions/1551382/python-user-friendly-time-format
    """
    now = datetime.datetime.now()

    if type(time) is datetime.datetime:
        diff = now - time
    elif type(time) is int:
        diff = now - datetime.datetime.fromtimestamp(time)
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"

@app.route('/package/<name>')
def packages_details(name):
    result = Distribution.query.filter_by(name=name).first()
    comments = Comment.query.filter_by(distribution_id=result.id)

    return render_template('package_details.html',
                           result=result,
                           comments=comments,
                           get_status=get_status,
                           time_delta=pretty_date)


@app.route('/package', methods=['GET', 'POST'])
def packages():
    if request.method == 'POST':
        return redirect(url_for('packages_details', name=request.form['pkgname']))
    else:
        return redirect(url_for('packages_browse_page', page_number=1))
