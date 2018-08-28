#!/usr/bin/env python

import sys
import subprocess
import os

if len(sys.argv) < 3:
    print('Usage: [path] [search string] [optional escaped pipe args]')
    print(' [pipe args] example: "| grep -v something"')
    sys.exit(1)

path = sys.argv[1]
search = sys.argv[2]
optional_pipe_args = sys.argv[3] if len(sys.argv) >= 4 else ''

try:
    output = subprocess.check_output('find ' + path + ' -type f', shell=True)
except subprocess.CalledProcessError as e:
    output = e.output

all_files = output.decode('utf-8', errors="ignore").split('\n')
current_pos = 0
max_pos = len(all_files) - 1
summary = ""

for f_path in all_files:
    if not os.path.isfile(f_path):
        continue

    current_pos += 1

    print(' -> (' + str(current_pos) + '/' + str(max_pos) + ') Looking in ' + f_path)
    
    try:
        strings_output = subprocess.check_output('strings ' + f_path + ' ' + optional_pipe_args, shell=True, timeout=30).decode('utf-8', errors='ignore')
    except subprocess.CalledProcessError as e:
        strings_output = e.output.decode('utf-8', errors='ignore')
    except subprocess.TimeoutExpired:
        strings_output = e.output.decode('utf-8', errors='ignore')

    if search in strings_output:
        msg = '!!! ' + f_path + ' has occurrence of ' + search
        summary += msg + "\n"
        print(msg)

print(summary)

