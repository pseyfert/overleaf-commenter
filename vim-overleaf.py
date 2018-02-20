# create an overleaf comment in the line below the curser
# TODO: current output puts »b'email-address@server.tld'« instead of »email-address@server.tld« (python3)

import subprocess
import datetime
import pytz
import vim

with open('/tmp/overleaf-debug.txt', 'w') as f:
    currentline = int(vim.eval('line(".")'))
    encoding = vim.eval("&encoding")
    currenttext = vim.current.buffer[currentline-1]
    replymode = currenttext[:4] == "% ^."
    f.write(currenttext)
    f.write('\n')
    if replymode:
        f.write("in reply mode\n")
    else:
        f.write("Not in reply mode\n")

    if replymode:
        leader = "% ^"
    else:
        leader = "% *"

    mylines = [
               "{} <{}> {}Z:".format(leader,
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

    if replymode:
        vim.current.buffer[currentline-1:currentline] = mylines
    else:
        vim.current.buffer[currentline:currentline] = mylines

    vim.eval('cursor({},3)'.format(currentline+3))
