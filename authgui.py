#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
GUI authenticator for DaKSiDE IMGUR Toolkit
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

import tkinter
from tkinter import Tk, Frame,Button,Label,Entry
from tkinter.ttk import Notebook
from tkinter.messagebox import askokcancel # get canned std dialog
from imgurpython import ImgurClient
from helpers import get_input, get_config

class SimpleImgurClient:
    def __init__(self):
        self.load_config()
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
            
class AuthForm:
    def __init__(self, client=SimpleImgurClient()):
        self.client = client
        # Create root component
        self.root = Tk()
        self.root.title('IMGUR Authenticator')
        
        self.textboxes = {}
        self.rows = []
        # Create textboxes
        self.addInputRow('client_id', text=self.client.client_id)
        self.addInputRow('client_secret', text=self.client.client_secret)
        self.addInputRow('URL', text=self.client.authorization_url)
        self.addInputRow('AuthCode')
        self.addInputRow('access_token', text=self.client.access_token)
        self.addInputRow('refresh_token', text=self.client.refresh_token)
        self.root.bind('<Return>', (lambda event: login()))
        
        # Login button
        self.btnLogin = Button(self.new_row(), text='Login', command= (lambda: self.login())).pack(side=tkinter.RIGHT)
        self.addInputRow('Username')
        self.btnWho = Button(self.new_row(), text='WhoAmI', command= (lambda: self.whoami())).pack(side=tkinter.RIGHT)
        
        # Pack everything
        self.pack_rows()
    
    def whoami(self):
        acc = self.client.whoami()
        self.setText(self.textboxes['Username'], acc.url)
    
    def login(self):
        pin = self.textboxes['AuthCode'].get()
        self.client.authorize(pin)
        self.setText(self.textboxes['access_token'], self.client.access_token)
        self.setText(self.textboxes['refresh_token'], self.client.refresh_token)
    
    def setText(self, textbox, text):
        textbox.delete(0, tkinter.END)
        textbox.insert(0, text)
    
    def new_row(self):
        row = Frame(self.root)
        self.rows.append(row)
        return row
        
    def pack_rows(self):
        for row in self.rows:
            row.pack(side=tkinter.TOP, fill=tkinter.X) # pack row on top
    
    def addInputRow(self, field, text=''):
        if field in self.textboxes:
            raise Exception("Input field exists")
        else:
            # Create a row
            row = self.new_row()
            
            # Create a label
            lbl = Label(row, width=10, text=field)
            
            # Create a textbox
            txtInput = Entry(row, width=75)
            self.setText(txtInput, text)
            self.textboxes[field] = txtInput
            
            # Pack UI
            lbl.pack(side=tkinter.LEFT)
            txtInput.pack(side=tkinter.RIGHT, expand=tkinter.YES, fill=tkinter.X) # grow horizontal
            return txtInput

    def run(self):
        self.root.mainloop()
        
#-----------------------------------------------------------------------------------
def main():
    frm = AuthForm()
    frm.run()

#-----------------------------------------------------------------------------------
if __name__ == "__main__":
    main()