#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
File duplicated files in folders
Latest version can be found at https://github.com/letuananh/pydemo

References:
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
__copyright__ = "Copyright 2015, pydemo"
__credits__ = [ "Le Tuan Anh" ]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Le Tuan Anh"
__email__ = "<tuananh.ke@gmail.com>"
__status__ = "Prototype"

########################################################################

import sys
import os
import argparse
from os import listdir
from os.path import isfile, join
from chirptext.leutile import jilog, header, Counter, Timer, TextReport, Table, FileTool, ChirpConfig
########################################################################

REPORT_LOC = './dirs.out.txt'

########################################################################
def compare(dirs, args):
    c = Counter()
    report = TextReport(REPORT_LOC)
    current_files = set()
    full_paths = {}
    for dir in dirs:
        if args.verbose:
            report.header("Dir: %s" % dir)
        dirfiles = set([ f for f in listdir(dir) if isfile(join(dir,f)) ])
        for file in dirfiles:
            file_path = join(dir, file)
            c.count('File')
            if file not in current_files:
                if args.verbose:
                    report.print('- %s' % (file),1)
                current_files.add(file)
                full_paths[file] = [ file_path ]
            else:
                if args.verbose:
                    report.print(">>> DUPLICATE: %s" % (file), 1)
                full_paths[file].append(file_path)
                c.count("Duplicate")
    report.header("Summary")
    vals = c.sorted_by_count()
    for val in vals:
        report.print("%s: %s" % (val[0], val[1]))
        
    report.header("Duplications")
    for k,v in full_paths.items():
        if len(v) < 2:
            continue
        report.print(k)
        for filepath in v:
            report.print(filepath, 1)
    

########################################################################

def main():
    '''Main entry of this demo application.
    '''

    # It's easier to create a user-friendly console application by using argparse
    # See reference at the top of this script
    parser = argparse.ArgumentParser(description="Display a line of text.")
    
    # Positional argument(s)
    parser.add_argument('-d1', '--dir1', help='First directory.')
    parser.add_argument('-d2', '--dir2', help='Second directory.')
    parser.add_argument('-l', '--listfile', help='A file contains a list of directories to compare')

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
        if args.dir1 and args.dir2:
            compare([args.dir1, args.dir2], args)
        elif args.listfile:
            with open(args.listfile, 'r') as listfile:
                dirs = [ x.strip() for x in listfile.readlines() ]
                compare(dirs, args)
        else:
            print("Please specify dirs or config file")
    pass

if __name__ == "__main__":
    main()
