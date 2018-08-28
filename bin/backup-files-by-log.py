#!/usr/bin/env python

import os
import sys
import re
import subprocess

if len(sys.argv) < 4:
    print('Tool for copying remote files byte-by-byte ignoring read errors from remote server using SSH.')
    print('Requirements: ssh client, sshpass')
    print('Made for Libertarian movement (Anarchist workers international - International Workers Association)')
    print('see https://iwa-ait.org, http://zsp.net.pl')
    print('')
    print('')
    print("Usage: [log_file_path] [ssh_password] [ssh_host] [chroot_path - optional]")
    print('       Instead of log path you can put "-" and provide contents via stdin.')
    print('       Log can be a output of eg. tar command that failed to copy some files')
    print('       or a find command, or any other that contains absolute UNIX paths to files')
    print('')
    sys.exit(1)

file_path = sys.argv[1]
password = sys.argv[2]
host = sys.argv[3]
chroot = sys.argv[4] if len(sys.argv) >= 5 else ''
content = open(file_path, 'r').read() if sys.argv[1] != '-' else sys.stdin.read()
extracted_paths = re.findall('\ ?\/([A-Za-z0-9\-_\.\/~]+)(\ |:)?', content)

current_pos = 0
max_pos = len(extracted_paths)

print('Found ' + str(max_pos) + ' paths to process')

for extracted_path in extracted_paths:
    current_pos +=1 

    path = '/' + extracted_path[0]
    target_backup_path = './' + path
    backup_cmd = 'sshpass -p "' + password + '" ssh ' + host + ' dd if=' + chroot + path + ' status=noxfer conv=noerror,sync > ' + target_backup_path

    try:
        print('... (' + str(current_pos) + '/' + str(max_pos) + ') Processing ' + path + ' into ' + target_backup_path)
        subprocess.call('mkdir -p ' + os.path.dirname(target_backup_path), shell=True)

        print('    + ' + backup_cmd)
        subprocess.call(backup_cmd, shell=True)

    except (KeyboardInterrupt, SystemExit):
        print('Interrupted... exiting.')
        sys.exit(1)

print('Done.')
