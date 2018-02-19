import subprocess
import datetime
from pytz import timezone

# microseconds are okay, but time zone isn't
# TODO: use isoformat after adjusting time zone (i.e. remove timezone from
#       datetime object again
# TODO: look up the time zone rather than assuming standard cern time zone

print("% ^* <"
      + subprocess.check_output(["git",
                                 "config",
                                 "--global",
                                 "--get",
                                 "user.email"]
                                )[:-1]
      + "> "
      + timezone('Europe/Zurich')
        .localize(datetime.datetime.now())
        .astimezone(timezone('UTC'))
        .strftime("%Y-%m-%dT%H:%m:%S.%f")
      + "Z:")
print("%")
print("% WRITEME")
print("%")
print("% ^.")
