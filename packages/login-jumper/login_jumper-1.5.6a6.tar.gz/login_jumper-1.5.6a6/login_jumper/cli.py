# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import os
import sys
import optparse

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)

from login_jumper.bin.server_gate import login_choice

VERSION = '1.5.6Alpha6'


def main():
    parser = optparse.OptionParser(
        version='%prog version ' + VERSION,
        usage='python server_gate.py [-H [host]]',
        description='Login server via jumper')
    parser.add_option(
        '--host', '-H',
        default='env4',
        type=str,
        dest='host',
        help="specify the host"
             "(default: env4)")
    parser.add_option(
        '--action', '-T',
        choices=['login', 'query'],
        default='login',
        type=str,
        dest='action',
        help="specify the type, login or query"
             "(default: login)")
    options, args = parser.parse_args()
    host = args.host
    action = args.action

    login_choice(host, action)


if __name__ == '__main__':
    main()
