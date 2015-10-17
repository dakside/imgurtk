#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
DaKSiDE IMGUR Toolkit
Latest version can be found at https://github.com/dakside/imgurtk

References:
    Adapted from example code from imgurpython project:
        https://github.com/Imgur/imgurpython
	Python documentation:
		https://docs.python.org/
	argparse module:
		https://docs.python.org/3/howto/argparse.html
	PEP 257 - Python Docstring Conventions:
		https://www.python.org/dev/peps/pep-0257/

@author: Le Tuan Anh <tuananh.ke@gmail.com>
'''

# Copyright (c) 2015, Le Tuan Anh <tuananh.ke@gmail.com>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

__author__ = "Le Tuan Anh <tuananh.ke@gmail.com>"
__copyright__ = "Copyright 2015, imgurtk"
__credits__ = [ "Le Tuan Anh" ]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Le Tuan Anh"
__email__ = "<tuananh.ke@gmail.com>"
__status__ = "Prototype"

########################################################################

import datetime
import codecs
from imgurpython import ImgurClient
from helpers import get_input, get_config

class SimpleImgurClient:
    def __init__(self, username=''):
        self.load_config()
        self.username = username
        self.client = ImgurClient(self.client_id, self.client_secret)
        self.client.set_user_auth(self.access_token, self.refresh_token)
        self.authorization_url = self.client.get_auth_url('pin')
    
    def load_config(self):
        config = get_config()
        config.read('auth.ini')
        self.client_id = config.get('credentials', 'client_id')
        self.client_secret = config.get('credentials', 'client_secret')
        self.access_token = config.get('credentials', 'access_token')
        self.refresh_token = config.get('credentials', 'refresh_token')
    
    def authenticate(self):
        print("Get your access PIN here: %s" % (self.authorization_url,))
        pin = get_input("Please enter your PIN: ")
        self.authorize(pin)
    
    def authorize(self, pin):
        credentials = self.client.authorize(pin, 'pin')
        self.client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
        self.access_token = credentials['access_token']
        self.refresh_token = credentials['refresh_token']
        self.save()
    
    def save(self):
        with open('auth.ini', 'w') as sessionfile:
            sessionfile.write("[credentials]\n")
            sessionfile.write("client_id={0}\n".format(self.client_id))
            sessionfile.write("client_secret={0}\n".format(self.client_secret))
            sessionfile.write("access_token={0}\n".format(self.access_token))
            sessionfile.write("refresh_token={0}\n".format(self.refresh_token))

    def whoami(self):
        '''Request account information from IMGUR server'''
        acc = self.client.get_account('me')
        # print("Account ID : %s" % (acc.id))
        # print("Account URL: %s" % (acc.url))
        # print("Account bio: %s" % (acc.bio))
        return acc
        
    def backup_myfavs(self, max_page_count=1):
        imgs = []
        with codecs.open('myfav.htm', 'w', 'utf-8') as myfav:
            for page in range(max_page_count):
                print("Fetching page #%s" % (page,))
                myfav.write("<h1>Page #%s</h1>" % (page))
                myfav.write("<table>")
                myfav.write("<tr><td>Title</td><td>Description</td><td>Datetime</td><td>Link</td></tr>")
                favs = self.client.get_account_favorites('me', page)
                for img in favs:
                    imgs.append(img)
                    myfav.write("<tr><td>%s</td><td>%s</td><td>%s</td><td><a href='%s'>%s</a><br/></td></tr>\n" % (img.title, img.description, datetime.datetime.fromtimestamp(img.datetime), img.link, img.link))
                    # myfav.write('<a href="%s">%s</a><br/>\n' % (img.link, img.link))
                myfav.write("</table>")
        return imgs

#-----------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is a library, not an application")