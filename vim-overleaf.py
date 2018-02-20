# create an overleaf comment in the line below the curser
# TODO: correctly answer to comment (replace current '% ^.' line and start with '^')
# TODO: current output puts »b'email-address@server.tld'« instead of »email-address@server.tld« (python3)

import subprocess
import datetime
import pytz
import vim

mylines = [
           "% ^* <{}> {}Z:".format(
                                   subprocess.check_output(["git",
                                                            "config",
                                                            "--get",
                                                            "user.email"]
                                                           )[:-1],
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

currentline = int(vim.eval('line(".")'))

vim.current.buffer[currentline:currentline] = mylines
