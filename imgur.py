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
from imgurpython import ImgurClient
from helpers import get_input, get_config
from auth import authenticate, reauth, whoami, ensure_loggedin

def backup_myfavs(client, max_page_count=2):
    with open('myfav.htm', 'w') as myfav:
        for page in range(max_page_count):
            print("Fetching page #%s" % (page,))
            myfav.write("<h1>Page #%s</h1>" % (page))
            favs = client.get_account_favorites('me', page)
            for img in favs:
                # print(img.link)
                myfav.write('<a href="%s">%s</a><br/>\n' % (img.link, img.link))

def myinfo(client):
    acc = whoami(client)
    print("Account ID : %s" % (acc.id))
    print("Account URL: %s" % (acc.url))
    print("Account bio: %s" % (acc.bio))                
                
def main():
    if len(sys.argv) != 2:
        print("Please run python imgur [username]")
    else:
        username = sys.argv[1]
        client = ensure_loggedin(username)
        if client:
            backup_myfavs(client)
        else:
            print("Cannot login to IMGUR")
    

def main():
    '''Main entry of DaKSiDE IMGUR Toolkit.
    '''

    # It's easier to create a user-friendly console application by using argparse
    # See reference at the top of this script
    parser = argparse.ArgumentParser(description="DaKSiDE IMGUR Toolkit")
    
    # Positional argument(s)
    parser.add_argument('username', help='Your IMGUR username')
    parser.add_argument('task', help='What you want to do (backup/info)')

    # Optional argument(s)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")

    # Main script
    if len(sys.argv) == 1:
        # User didn't pass any value in, show help
        parser.print_help()
    else:
        # Parse input arguments
        args = parser.parse_args()
        # Now do something ...
        if args.username:
            client = ensure_loggedin(args.username)
            if client:
                if args.task == 'backup':
                    backup_myfavs(client)
                else:
                    myinfo(client)
            else:
                print("Cannot login to IMGUR")
    pass

if __name__ == "__main__":
    main()

    

    
