This repo contains a simple script named `list-unsubscribe.py` that can be used
to aid in unsubscribing from marketing emails. The script looks for a
`List-Unsubscribe` header in an email message, and extracts the URL contained in
this header. This is useful in conjunction with command line email clients (I
use it with [mu4e](https://www.djcbsoftware.nl/code/mu/mu4e.html)).

Usage:

```bash
# Print the List-Unsubscribe URL, raw email read from stdin
$ python3 list-unsubscribe.py

# Alternate form, reading the raw email from the given file
$ python3 list-unsubscribe.py path/to/email/file

# Use -b to open the URL locally in a web browser
$ python3 list-unsubscribe.py -b
```

This code is free software licensed under the terms of the GPLv3+, as described
in the LICENSE file.
