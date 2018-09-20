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

from typing import Tuple

URL_REGEX = re.compile(r'<(https?://.*?)>')


def get_unsubscribe_url(msg: email.message.EmailMessage) -> Tuple[str, str]:
    """Get the unsubscribe URL fron an email message.

    Returns tuple of (raw header value, parsed URL).
    """
    try:
        raw_value = msg['List-Unsubscribe']
    except KeyError:
        return '', ''  # no List-Unsubscribe

    m = URL_REGEX.search(raw_value)
    if m:
        return raw_value, m.groups()[0]
    return raw_value, ''


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

    if args.file == '-':
        msg = email.message_from_file(sys.stdin)
    else:
        with open(args.file) as input_file:
            msg = email.message_from_file(input_file)
    raw_value, url = get_unsubscribe_url(msg)

    if not raw_value:
        return  # no header found

    if args.print_value:
        print(raw_value)

    if url:
        if args.browser:
            webbrowser.open_new_tab(url)
        else:
            print(url)


if __name__ == '__main__':
    main()
