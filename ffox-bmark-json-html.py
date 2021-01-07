#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert firefox json bookmarks export to html
Needed because the html export omits the mobile bookmarks

Known limitations:
    Can only handle 5 levels of nested folders because that's how
       many levels HTML headers have (h1 for page header, h2 for top-level
       folders, then so forth.
    Haven't tested with an empty folder in bookmarks.
"""

import logging
from pprint import pformat
import typing
import sys
import contextlib
import json
import csv
import requests

# global configuration.  Should I be doing this differently?

# constants
# TODO: Looked into libraries for html generation, but seemed complicated.
#   Should revisit. Airium?
HTML_HEAD = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"> 
<title>Full Firefox Bookmarks</title>
</head>
<body>
'''

HTML_FOOT = '''
</body>
</html>
'''

HTML_HEADERS = {1 : { 'open' : '<h1>', 'close' : '</h1>' },
                2 : { 'open' : '<h2>', 'close' : '</h2>' },
                3 : { 'open' : '<h3>', 'close' : '</h3>' },
                4 : { 'open' : '<h4>', 'close' : '</h4>' },
                5 : { 'open' : '<h5>', 'close' : '</h5>' },
                6 : { 'open' : '<h6>', 'close' : '</h6>' }}

FOLDER_TYPE = "text/x-moz-place-container"
BOOKMARK_TYPE = "text/x-moz-place"

# set up error/warning output
logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)

# to open file in with while defaulting to stdout if no filename given
@contextlib.contextmanager
def file_writer(file_name = None):
    # Create writer object based on file_name
    writer = open(file_name, "w") if file_name is not None else sys.stdout
    # yield the writer object for the actual use
    yield writer
    # If it is file, then close the writer object
    if file_name != None: writer.close()

def convert_bookmark_folder(folder: dict, head_level: int):
    """Step through the tree of bookmark folders & bookmarks and convert
    to HTML.

    Parameters:
        folder: a Firefox bookmarks folder loaded from 
        head_level: what level of header to use for this folder

    Returns:
        HTML version of the folder with bookmarks and sub-folders
    """
    log.warning("In convert_bookmark_folder")  # debug
    title = folder.get('title')
    if (title is None or title == '') and head_level == 1:
        outstring = "<h1>Full Firefox Bookmarks</h1>"
    else:
        outstring = "%s%s%s" % (HTML_HEADERS.get(head_level,{}).get('open'),
                               title or "No folder title",
                               HTML_HEADERS.get(head_level,{}).get('close'))
    for child in folder.get('children'):
        if child.get(type) == FOLDER_TYPE:
           outstring += convert(bookmark_folder(child, head_level+1)
        else if child.get(type) == BOOKMARK_TYPE:
### Start here.  Need to convert bookmark to html <p>


    return outstring



## inherited code    debug
"""
    if isinstance(item, dict):
        log.warning("It's a dict")
        leaves = {}
        for i in item.keys():
            leaves.update(get_leaves(item[i], i))
        return leaves
    elif isinstance(item, list):
        log.warning("It's a list")
        leaves = {}
        for i in item:
            leaves.update(get_leaves(i, key))
        return leaves
    else:
        log.warning("It's neither")
        log.warning("%s; %s", pformat(item), type(item))
        return {key : item}
"""
## end inherited code

def main():
    # need to parse arguments, print errors & help
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        log.error("Convert firefox json bookmarks export to html.")
        log.error("usage: %s json_file [html_file]" % sys.argv[0])
        sys.exit(2)
    json_filename = sys.argv[1]
    html_filename = len(sys.argv) > 2 and sys.argv[2] or None

    # python 3.9 allows with break on comma without backslash, but I've
    #       still got 3.8
    with open(json_filename) as json_file, file_writer(html_filename) as html_file:
        json_data = json.load(json_file)

        # start html with header
        html_file.write(HTML_HEAD)

        # bookmarks are in the json element 'children'
        # travel down the tree and output bookmarks as html
        html_bookmarks = convert_bookmark_folder(json_data, head_level=1)
        html_file.write(html_bookmarks)

        # finish off the html
        html_file.write(HTML_FOOT)

    sys.exit(0)

if __name__ == '__main__':
    main()

