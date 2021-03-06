#!/usr/bin/python3
#
# Copyright (c) 2018 Evan Klitzke <evan@eklitzke.org>
#
# This file is part of list-unsubscribe.py.
#
# list-unsubscribe.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# list-unsubscribe.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# list-unsubscribe.py. If not, see <http://www.gnu.org/licenses/>.

import argparse
import email
import email.message
import re
import sys
import webbrowser

URL_REGEX = re.compile(r'<((https?://|mailto:).*?)>')


def get_raw_unsubscribe_value(filename: str) -> str:
    """Get the raw List-Unsubscribe value for a filename."""
    if filename == '-':
        msg = email.message_from_file(sys.stdin)
    else:
        try:
            with open(filename) as input_file:
                msg = email.message_from_file(input_file)
        except UnicodeDecodeError:
            return get_unsubscribe_value_from_invalid_file(filename)

    try:
        return msg['List-Unsubscribe']
    except KeyError:
        return ''


def get_unsubscribe_value_from_invalid_file(filename: str, lines=100) -> str:
    """Try to get a List-Unsubscribe even if the file is improperly encoded."""
    with open(filename, 'rb') as f:
        # assume the List-Unsubscribe header is in the first few lines
        for _ in range(lines):
            line = f.readline()
            if line.startswith(b'List-Unsubscribe:'):
                line = line.decode('utf8').rstrip()
                return line.split(': ', 1)[1]
    return ''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b',
        '--browser',
        action='store_true',
        help='Open URL in browser if possible')
    parser.add_argument(
        '-p',
        '--print-value',
        action='store_true',
        help='Print raw header field value')
    parser.add_argument(
        'file',
        nargs='?',
        default='-',
        help='File to process, or stdin if omitted')
    args = parser.parse_args()

    raw_value = get_raw_unsubscribe_value(args.file)
    if not raw_value:
        sys.exit(1)  # List-Unsubscribe header not found

    if args.print_value:
        print(raw_value)
        return

    m = URL_REGEX.search(raw_value)
    if not m:
        sys.exit(2)  # List-Unsubscribe header found, but no URL found

    url = m.groups()[0].strip()
    if args.browser:
        webbrowser.open_new_tab(url)
    else:
        print(url)


if __name__ == '__main__':
    main()
