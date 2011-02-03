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

import os
import random
from flask import render_template

from .application import app
from .application import db

from .model import Distribution
#from .model import User
from .model import Comment
from .utils import get_status, pretty_date
from flask import g, session
from flask import send_file
from cStringIO import StringIO
from flask import Response
from werkzeug import Headers

import captchaimage
import cStringIO
from PIL import Image
all_keys = {}

# Black text on white background
def get_captcha_image(code):
    size_y = 32
    image_data = captchaimage.create_image(
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 28, size_y, code)
    file = cStringIO.StringIO()
    Image.fromstring(
        "L", (len(image_data) / size_y, size_y), image_data).save(
        file, "JPEG", quality = 30)
    return file.getvalue()

@app.route('/captcha/<key>')
def captcha(key):
    global all_keys
    img = get_captcha_image(all_keys[key])
    headers = Headers()
    headers.add("Content-Type", "image/jpeg")
    return Response(img, headers=headers)

def verify_captcha(key, value):
    global all_keys
    if key not in all_keys:
        return False
    if all_keys[key] == value:
        del all_keys[key]
        return True
    else:
        del all_keys[key]
        return False

def randomword():
    random_range = random.randrange(4,7)
    text = list(open(os.path.join(os.path.dirname(__file__), "shuffle.txt")).read())
    length = len(text)
    final_word_list = []
    for i in range(random_range):
        pos = random.randrange(0,length)
        final_word_list.append(text[pos])
    return ''.join(final_word_list)

def get_captcha_key():
    global all_keys
    import uuid
    uuid4 = str(uuid.uuid4())
    all_keys[uuid4] = randomword()
    return uuid4
