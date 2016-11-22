#!/usr/bin/env python3

# Copyright (c) 2016 Stephen Warren <swarren@wwwdotorg.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import argparse
import fnmatch
import os
import requests
import sys
try:
    from os import scandir
except ImportError:
    from scandir import scandir

def push_file(host, local_path, remote_name):
    print('..PUSH FILE: ' + remote_name)
    files = {'file': (remote_name, open(local_path,'rb'))}
    response = requests.post('http://%s/upload.cgi' % host, files=files)
    print('.... ' + str(response.status_code))
    response.raise_for_status()
    if 'NG' in response.text or 'action=/upload.cgi' not in response.text:
        print('Upload failed:', file=sys.stderr)
        print(response.text, file=sys.stderr)
        sys.exit(1)

def op_push_dir(host, local_dir):
    print('PUSH DIR: ' + local_dir)
    for de in scandir(local_dir):
        if not de.is_file():
            print('Can\'t handle non-file "%s"' % de.path, file=sys.stderr)
            sys.exit(1)
        push_file(host, de.path, de.name)

def op_rm_list(host, rm_list_file):
    print('RM LIST: ' + rm_list_file)
    params = {'op': 100, 'DIR': '/'}
    response = requests.get('http://%s/command.cgi' % host, params=params)
    response.raise_for_status()
    lines = response.text.splitlines()
    if lines[0] != 'WLANSD_FILELIST':
        print('File list qery failed:', file=sys.stderr)
        print(response.text, file=sys.stderr)
        sys.exit(1)
    existing_files = []
    for l in lines[1:]:
        existing_files.append(l.split(',')[1].lower())
    with open(rm_list_file, 'rt') as fh:
        for l in fh:
            l = l.split('#')[0]
            rmspec = l.strip().lower()
            if not rmspec:
                continue
            for remote_filename in existing_files[:]:
                if fnmatch.fnmatch(remote_filename, rmspec):
                    print('..DELETE: ' + remote_filename)
                    params = {'DEL': '/' + remote_filename}
                    response = requests.get('http://%s/upload.cgi' % host, params=params)
                    print('.... ' + str(response.status_code))
                    response.raise_for_status()
                    if 'SUCCESS' not in response.text:
                        print('Delete failed:', file=sys.stderr)
                        print(response.text, file=sys.stderr)
                        sys.exit(1)

op_map = {
    'push': op_push_dir,
    'rmlist': op_rm_list,
}

def main():
    parser = argparse.ArgumentParser(
        description='Copy files to a Toshiba FlashAir device')
    parser.add_argument('host', help='The host or host:port of the FlashAir')
    parser.add_argument('ops', nargs='+', help='''Operations to perform;
    "dir", "push:dir": push directory, "rmlist:listfile": delete files listed
    in listfile''')
    args = parser.parse_args()

    for op in args.ops:
        if not ':' in op:
            func = op_push_dir
            param = op
        else:
            (op_name, param) = op.split(':', 1)
            if op_name not in op_map:
                print('"%s" is not a valid operation' % op_name,
                    file=sys.stderr)
                parser.print_help(file=sys.stderr)
                sys.exit(1)
            func = op_map[op_name]
        func(args.host, param)

if __name__ == '__main__':
    main()
