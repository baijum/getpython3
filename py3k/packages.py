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
from .utils import get_status, pretty_date
from .captcha import get_captcha_key
from .captcha import verify_captcha

from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed


def make_external(url):
    return urljoin(request.url_root, "project/%s"%url)


@app.route('/project/<name>/recent.atom')
def recent_project_comment_feed(name):
    feed = AtomFeed("Project: %s"%name,
                    feed_url=request.url, url=request.url_root)
    result = Distribution.query.filter_by(name=name).first()
    if result is None:
        return redirect(url_for('search_package', name=name, page=1))
    comments = Comment.query.filter_by(distribution_id=result.id).order_by(db.desc(Comment.datetime)).limit(5)

    for comment in comments:
        title = "%s has %s (%s) %s on %s" % (comment.fullname,
                                             name, comment.version,
                                             "Working" if comment.working else "Failing",
                                             comment.platform)
        feed.add(title, unicode(comment.comment),
                 content_type='html',
                 author=comment.fullname,
                 url=make_external(name),
                 updated=comment.datetime,
                 published=comment.datetime)
    return feed.get_response()

@app.route('/project/<name>/add_comment', methods=['POST'])
def add_comment(name):
    fullname = request.form['fullname'].strip() or 'Anonymous'
    email = request.form['email']
    working = request.form['working']
    platform = request.form['platform']
    version = request.form['version']
    comment = request.form['comment']
    captchakey = request.form['captchakey']
    captchavalue = request.form['captchavalue']
    if not verify_captcha(captchakey, captchavalue):
        return redirect(url_for('packages_details', name=name))
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

@app.route('/search/<name>/+<int:page>')
def search_package(name, page=1):
    result = Distribution.query.filter(Distribution.name.like("%%%s%%"%name)).paginate(page)
    return render_template('search_package.html', page_obj=result, searchname=name)

@app.route('/project/<name>')
def packages_details(name):
    result = Distribution.query.filter_by(name=name).first()
    if result is None:
        return redirect(url_for('search_package', name=name, page=1))
    comments = Comment.query.filter_by(distribution_id=result.id).order_by(db.desc(Comment.datetime))
    return render_template('package_details.html',
                           result=result,
                           comments=comments,
                           get_status=get_status,
                           time_delta=pretty_date,
                           captcha_key=get_captcha_key())



@app.route('/project', methods=['GET', 'POST'])
@app.route('/project/+<int:page>')
def packages(page=1):
    if request.method == 'POST':
        return redirect(url_for('search_package', name=request.form['pkgname'], page=1))
    else:
        result = Distribution.query.order_by(Distribution.name).paginate(page)
        return render_template('show_package.html', page_obj=result)
