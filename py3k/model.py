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

from .application import db

class Distribution(db.Model):
    __tablename__ = 'distributions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    home_page = db.Column(db.String(50))
    author = db.Column(db.String(50))
    summary = db.Column(db.String(50))

    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(120))
    fullname = db.Column(db.String(50))

    def __init__(self, username, email, openid, fullname=''):
        self.username = username
        self.email = email
        self.openid = openid
        self.fullname = fullname

    def __repr__(self):
        return '<User %r>' % (self.username)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    distribution_id = db.Column("distribution_id", db.Integer, db.ForeignKey('distributions.id'))
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('users.id'))
    comment = db.Column(db.String(5000))
    status = db.Column(db.Boolean()) #True=Working,False=FAILING
