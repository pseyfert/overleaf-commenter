#!/usr/bin/env python3
from datetime import datetime
import sys
import re
import difflib
with open("example.tex", "r") as ex:
    with open("desired.tex", "r") as des:
        lines = list(difflib.unified_diff(
            ex.readlines(),
            des.readlines(),
            n=0))

for line in lines[2:]:
    line = line[:-1]
    if re.match('@@ [+-][0-9]* [+-][0-9]* @@', line) is not None:
        continue
    try:
        datetime.strptime(
                re.sub(
                    "[+-]% [*^] <tester@testserver.org> ",
                    "",
                    line[:-1]),
                '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        print("offending diff: {}".format(line))
        sys.exit(5)
sys.exit(0)
