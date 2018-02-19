import subprocess
import datetime
import pytz

print("% ^* <"
      + subprocess.check_output(["git",
                                 "config",
                                 "--global",
                                 "--get",
                                 "user.email"]
                                )[:-1]
      + "> "
      + datetime.datetime.now(tz=pytz.utc)
        .replace(tzinfo=None)
        .isoformat()
      + "Z:")
print("%")
print("% WRITEME")
print("%")
print("% ^.")
