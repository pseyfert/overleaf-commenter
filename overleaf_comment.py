# copyright 2018 CERN for the benefit of the LHCb collaboration (see LICENSE)

# This file is part of overleaf-commenter.
#
# overleaf-commenter is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# overleaf-commenter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with overleaf-commenter.  If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.

'''
Add a comment compatible with the overleaf discussion functionality to a .tex
file below the cursor in vim.

Features:
 - When called from the command line, a comment skeleton is printed.
 - Name of the commentator is extracted from the git config (might be wrong as
   overleaf access restriction and git commit email address are independent)
 - Identify a reply when the cursor is on the last line of an existing comment
   (the one '% ^.')

USAGE:
e.g. in .vimrc define
```
function! OverleafComment()
  py3f /path/to/overleaf-commenter/overleaf_comment.py
endfunc
function! OverleafCloseDiscussion()
  py3 import sys
  py3 sys.argv.append('--close')
  py3f /path/to/overleaf-commenter/overleaf_comment.py
  py3 sys.argv.pop()
endfunc
```
'''

# TODO: logging
# TODO: check if there are encoding issues

import subprocess
import datetime
import pytz


def close_discussion(leader='^'):
    """ close_discussion
    Generates a string to close a discussion.

    It assumes execution in the overleaf document's git repository (for email
    address lookup).

    The time at calling the function is used for the timestamp of closing the
    discussion.

    Args:

        leader: string that will mostly be ignored (use same interface as
                generate_comment). Except, if the leader is '*' an exception
                is raised.

    Returns: list of strings (one element for the one line)

    Raises: AssertionError when called from vim and not from the last line of
            a discussion (identified through the leader argument).

    """
    if leader == '*':
        raise AssertionError("Can only close discussion from the last line of"
                             " a discussion.")

    mylines = [
               "% ^ <{}> {}Z.".format(subprocess.check_output(["git",
                                                               "config",
                                                               "--get",
                                                               "user.email"]
                                                              )[:-1].decode(),
                                      datetime
                                      .datetime
                                      .now(tz=pytz.utc)
                                      .replace(tzinfo=None)
                                      .isoformat()
                                      ),
    ]
    return mylines


def generate_comment(leader='*^'):
    """ generate_comment
    Generates an almost empty overleaf comment.

    It assumes execution in the overleaf document's git repository (for email
    address lookup).

    The comment itself is defaulted to 'WRITEME'.

    The time at calling the function is used for the timestamp of the comment
    (moderately irrelevant in terms of code behaviour - overleaf accepts future
    and past comments).

    Args:

        leader: special characters on the first line of the comment syntax
                between '%' and the email address. Used to distinguish new
                comments (leader = '*' -> '% * <email>') from replies
                (leader = '^').

    Returns: list of strings (line-by-line)
    """
    mylines = [
               "% {} <{}> {}Z:".format(leader,
                                       subprocess.check_output(["git",
                                                                "config",
                                                                "--get",
                                                                "user.email"]
                                                               )[:-1].decode(),
                                       datetime
                                       .datetime
                                       .now(tz=pytz.utc)
                                       .replace(tzinfo=None)
                                       .isoformat()
                                       ),
               "%",
               "% WRITEME",
               "%",
               "% ^.",
    ]
    return mylines


def get_line_function():
    """get_line_function
    Parse arguments to decide if a discussion should be closed or if a regular
    comment will be posted

    Returns: a function which has a leader (string) argument and returns a list
             of strings (the comment for the tex document).

    """

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--close",
                        help="generate string to close a discussion",
                        action="store_true")
    args = parser.parse_args()
    if args.close:
        line_function = close_discussion
    else:
        line_function = generate_comment

    return line_function


def vim_main():
    """vim_main
    Main routine to add an overleaf comment to a document from vim.

    The comment is added in the line below the current cursor position.

    If the cursor is on an end-of-discussion line, a reply is posted. Otherwise
    a new discussion is started. When called from within a discussion, code for
    starting a new discussion will be posted and likely lead to invalid syntax.
    """

    currentline = int(vim.eval('line(".")'))
    # encoding = vim.eval("&encoding")
    currenttext = vim.current.buffer[currentline-1]
    replymode = currenttext[:4] == "% ^."

    if replymode:
        leader = "^"
    else:
        leader = "*"

    # 0 element in CLI will be filename of this script. In VIM it could be
    # anything. Possibly ['/must>not&exist/foo']
    try:
        line_function = get_line_function()
    except SystemExit:
        # argument parsing failed
        line_function = generate_comment
    mylines = line_function(leader)

    if replymode:
        vim.current.buffer[currentline-1:currentline] = mylines
    else:
        vim.current.buffer[currentline:currentline] = mylines

    if len(mylines) > 1:
        if replymode:
            vim.eval('cursor({},3)'.format(currentline+2))
        else:
            vim.eval('cursor({},3)'.format(currentline+3))


def cli_main():
    """cli_main
    Fallback to vim_main.

    In case the overleaf-commenter is called from the command line, the comment
    string will get printed to stdout without special editor features.
    """

    line_function = get_line_function()

    for line in line_function():
        print(line)


try:
    import vim
    make_overleaf = vim_main
except ImportError:
    make_overleaf = cli_main

if __name__ == '__main__':
    try:
        make_overleaf()
    except Exception as e:
        print(e)
