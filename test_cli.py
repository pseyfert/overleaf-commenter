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

import overleaf_comment
from unittest import TestCase


class TestOverleafComments(TestCase):
    def test_empty_comment(self):
        """when called without arguments one should get a single comment

        The template text might be arbitrary, the email address should be
        a valid email address, the date should look alright-ish.
        """

        import sys
        backup = sys.argv
        sys.argv = ["testenv"]
        line_function = overleaf_comment.get_line_function()
        lines = line_function()
        sys.argv = backup
        self.assertEqual(len(lines), 5)

        # check line by line

        # this checks for '% *^ <email> YYYY-MM-DDTHH:mm:ss.fffffZ:'
        # where the year is in the 21st century (excl. 2100, and incl. 2000)
        # the email matches the email regex from http://emailregex.com/
        # cf https://stackoverflow.com/a/201378
        # it should comply with RFC 5322
        # the number of digits after seconds is arbitrary (and can be zero)

        self.assertRegexpMatches(lines[0], "^% \*\^ <[a-zA-Z0-9_.+-]+@"
                                           "[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+> "
                                           "20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]"
                                           "T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]"
                                           "\.[0-9]*Z:$")

        self.assertEquals(lines[1], "%")
        for line in lines[2:-2]:
            self.assertRegexpMatches(line, "^%.*$")
        self.assertEquals(lines[-2], "%")
        self.assertEquals(lines[-1], "% ^.")

    def test_leader(self):
        """check that the leader is only the single given character"""

        firstline = overleaf_comment.generate_comment("A")[0]
        self.assertRegexpMatches(firstline, "^% A .*")

    def test_date(self):
        """check that the current date is valid isoformat"""
        import re
        from dateutil import parser

        firstline = overleaf_comment.generate_comment()[0]
        stringdate = re.search(".*\> (.*):", firstline).group(1)
        parser.isoparse(stringdate)

    def test_assert_close_at_end(self):
        with self.assertRaises(AssertionError) as context:
            overleaf_comment.close_discussion("*")
        self.assertIn("last line", str(context.exception))

    def test_closing(self):
        import sys
        import re
        from dateutil import parser
        backup = sys.argv
        sys.argv = ["testenv", "--close"]
        line_function = overleaf_comment.get_line_function()
        lines = line_function()
        sys.argv = backup
        self.assertEqual(len(lines), 1)

        # check line by line

        # this checks for '% ^ <email> YYYY-MM-DDTHH:mm:ss.fffffZ.'
        # where the year is in the 21st century (excl. 2100, and incl. 2000)
        # the email matches the email regex from http://emailregex.com/
        # cf https://stackoverflow.com/a/201378
        # it should comply with RFC 5322
        # the number of digits after seconds is arbitrary (and can be zero)

        self.assertRegexpMatches(lines[0], "^% \^ <[a-zA-Z0-9_.+-]+@"
                                           "[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+> "
                                           "20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]"
                                           "T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]"
                                           "\.[0-9]*Z.$")
        stringdate = re.search(".*\> (.*).", lines[0]).group(1)
        parser.isoparse(stringdate)
