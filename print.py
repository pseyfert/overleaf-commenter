import subprocess
import datetime
import pytz

print("% ^* <{}> {}Z:"
      .format(
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
             )
      )
print("%")
print("% WRITEME")
print("%")
print("% ^.")
