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

from flask import render_template, request
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed


from .application import app
from .application import db

from .model import Distribution
from .model import Comment
from .utils import get_status, pretty_date


@app.route('/')
def index():
    comments = db.session.query(Comment, Distribution).outerjoin(Distribution).order_by(db.desc(Comment.datetime)).limit(500)
    package_names = []
    lst_comments = []
    idx = 0
    for comment,distribution in comments:
        if distribution.name not in package_names:
            package_names.append(distribution.name)
            lst_comments.append(idx)
        idx += 1
    # FIXME: The above hack should be fixed with this better query
    # select * from distributions inner join (select * from comments where
    # comments.id in (select max(comments.id) as id from comments group by
    # comments.distribution_id)) a on distributions.id = a.distribution_id
    # order by a.datetime desc

    no_comments_packages = db.session.query(Distribution).outerjoin(Comment).filter(Comment.distribution_id==None).limit(5)

    # select name,successcnt,failcnt from distributions d
    # inner join
    # (
    #     select  distribution_id,
    #     sum(case when check=true then 1 else 0 end) as successcnt,
    #     sum(case when chec=false then 1 else end ) as failcnt
    #     from
    #     comments where datetime between(currendate,currentdate-60)
    #     group by distribution_id) a on a.distribution_id =d.distribution_idn

    return render_template('index.html',
                           comments=comments,
                           no_comments_packages=no_comments_packages,
                           lst_comments=lst_comments,
                           get_status=get_status,
                           time_delta=pretty_date)


def make_external(url):
    return urljoin(request.url_root, "project/%s"% url)


@app.route('/recent.atom')
def recent_all_comment_feed():
    feed = AtomFeed("Recent Project Comments",
                    feed_url=request.url, url=request.url_root)
    comments = db.session.query(Comment, Distribution).outerjoin(Distribution).order_by(db.desc(Comment.datetime)).limit(500)
    package_names = []
    lst_comments = []
    idx = 0
    for comment,distribution in comments:
        if distribution.name not in package_names:
            package_names.append(distribution.name)
            lst_comments.append(idx)
        idx += 1

    for idx in lst_comments[:6]:

        comments[idx][0].email
        comments[idx][1].name
        comments[idx][0].version
        comments[idx][0].working
        comments[idx][0].fullname
        comments[idx][0].platform
        comments[idx][0].datetime

        title = "%s has %s (%s) %s on %s" % (comments[idx][0].fullname,
                                             comments[idx][1].name, comments[idx][0].version,
                                             "Working" if comments[idx][0].working else "Failing",
                                             comments[idx][0].platform)
        feed.add(title, unicode(comments[idx][0].comment),
                 content_type='html',
                 author=comment.fullname,
                 url=make_external(comments[idx][1].name),
                 updated=comment.datetime,
                 published=comment.datetime)
    return feed.get_response()


@app.route('/credits')
def credits():
    return render_template('credits.html')
