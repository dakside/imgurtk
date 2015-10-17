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

'''
    Here's how you go about authenticating yourself! The important thing to
    note here is that this script will be used in the other examples so
    set up a test user with API credentials and set them up in auth.ini.
'''

import os
import argparse
import sys
from igui import AuthForm
from auth import SimpleImgurClient

from chirptext.leutile import FileTool
from puchikarui import *

#------------------------------------------------------------------------------

STORE_DIR = FileTool.abspath('./dirs.txt')

#------------------------------------------------------------------------------

class SchemaImgur(Schema):
    def __init__(self, data_source=None):
        Schema.__init__(self, data_source)
        self.add_table('image', 'title description datetime link'.split())
    
    def create(self):
        self.ds().executescript('''
        -- DROP TABLE IF EXISTS image; 
        CREATE TABLE IF NOT EXISTS image(title, description, datetime, link PRIMARY KEY);
        ''')

def is_cached(filename, dirs):
    for dir in dirs:
        if os.path.isfile(os.path.join(dir, filename)):
            return True
    return False

def get_db_file(client):
    if client.username and len(client.username.strip()) > 0:
        return os.path.join('data', client.username.strip() + '.db')
    else:
        return 'data/imgur.db'

def dev(client, page):
    dirs = [ FileTool.abspath('~/Pictures/') ]
    print(is_cached('test.jpg', dirs))
    
    # backup to DB
    db_path = get_db_file(client)
    with SchemaImgur(db_path) as db:
        if not os.path.isfile(db_path) or os.path.getsize(db_path) == 0:
            db.create()
        imgs = client.backup_myfavs(page)
        for img in imgs:
            img_row = db.image.select_single(where='link = ?', values=[img.link])
            if img_row:
                # update?
                print("This link is ignored because it exists in current database: %s" % (img.link))
                pass
            else:
                print("Saving: %s" % (img.link))
                db.image.insert([img.title, img.description, img.datetime, img.link])
        db.ds().commit()
    pass
        
#------------------------------------------------------------------------------

def ensure_loggedin(username):
    client = SimpleImgurClient(username)
    try:
        acc = client.whoami()
    except:
        acc = None
    if acc and acc.url == username:
        return client # Valid client
        
    while not acc or acc.url != username:
        # try to login again
        # may be access key is expired
        client.authenticate()
        acc = client.whoami()
    
    return client

def myinfo(client):
    acc = client.whoami()
    print("Account ID : %s" % (acc.id))
    print("Account URL: %s" % (acc.url))
    print("Account bio: %s" % (acc.bio))                
                
#------------------------------------------------------------------------------

def main():
    '''Main entry of DaKSiDE IMGUR Toolkit.
    '''

    # It's easier to create a user-friendly console application by using argparse
    # See reference at the top of this script
    parser = argparse.ArgumentParser(description="DaKSiDE IMGUR Toolkit")
    
    # Positional argument(s)
    parser.add_argument('-u', '--username', help='Your IMGUR username')
    parser.add_argument('-t', '--task', help='What you want to do (backup/info/gui)')
    parser.add_argument('-p', '--page', help='Max page count (for backup)')

    # Optional argument(s)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")

    # Parse input arguments
    args = parser.parse_args()
    # Now do something ...
    client = SimpleImgurClient() # no username
    if args.username:
        client = ensure_loggedin(args.username)

    if args.task == 'backup':
        backup_myfavs(client)
    elif args.task == 'info':
        myinfo(client)
    elif args.task == 'gui':
        frm = AuthForm()
        frm.run()
    else:
        # Run GUI by default
        # parser.print_help()
        # AuthForm().run()
        try:
            page = int(args.page)
        except Exception as e:
            page = 1
        dev(client, page)
    pass
#------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

    

    
