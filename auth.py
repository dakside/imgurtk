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

from imgurpython import ImgurClient
from helpers import get_input, get_config

def whoami(client):
    '''Request account information from IMGUR server'''
    acc = client.get_account('me')
    # print("Account ID : %s" % (acc.id))
    # print("Account URL: %s" % (acc.url))
    # print("Account bio: %s" % (acc.bio))
    return acc

def ensure_loggedin(username):
    '''Make sure that we have logged in before performing any request.
    This will return a client object if client is logged in, otherwise None.
    Exception may be thrown, catch them.
    '''
    try:
        client = reauth()
        if whoami(client).url != username:
            client = None
    except Exception as e:
        client = None
    if client is None:
        print("We need to re-authenticate ...")
        client = authenticate()
    if username == whoami(client).url:
        print("You have been logged in as user: %s" % (username))
        return client
    else:
        return None
    
def reauth():
    ''' Reuse access token
    '''
    # Get client ID and secret from auth.ini
    config = get_config()
    config.read('auth.ini')
    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')
    access_token = config.get('credentials', 'access_token')
    refresh_token = config.get('credentials', 'refresh_token')

    client = ImgurClient(client_id, client_secret)
    client.set_user_auth(access_token, refresh_token)

    print("Reusing access_token. Here are the details:")
    print("   Access token:  {0}".format(access_token))
    print("   Refresh token: {0}".format(refresh_token))

    return client

def authenticate():
    ''' Authenticate for the first time
    '''
    # Get client ID and secret from auth.ini
    config = get_config()
    config.read('auth.ini')
    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')

    client = ImgurClient(client_id, client_secret)

    # Authorization flow, pin example (see docs for other auth types)
    authorization_url = client.get_auth_url('pin')

    print("Go to the following URL: {0}".format(authorization_url))
    with open('url.txt', 'w') as urlfile:
        urlfile.write(authorization_url)
   

    # Read in the pin, handle Python 2 or 3 here.
    pin = get_input("Enter pin code: ")

    # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

    print("Authentication successful! Here are the details:")
    print("   Access token:  {0}".format(credentials['access_token']))
    print("   Refresh token: {0}".format(credentials['refresh_token']))
    with open('auth.ini', 'w') as sessionfile:
        sessionfile.write("[credentials]\n")
        sessionfile.write("client_id={0}\n".format(client_id))
        sessionfile.write("client_secret={0}\n".format(client_secret))
        sessionfile.write("access_token={0}\n".format(credentials['access_token']))
        sessionfile.write("refresh_token={0}\n".format(credentials['refresh_token']))

    return client

#-----------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is a library, not an application")