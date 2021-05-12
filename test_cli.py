import subprocess
import re
import os


origWD = os.getcwd() # remember our original working directory
# change directory to where signal-bat is installed
os.chdir(os.path.join(origWD, "signal-cli/build/install/signal-cli/bin"))

# send second signal text with audio attachment
subprocess.run(["signal-cli.bat", "-u", "+16503088054", "send", \
        "-m", "", "+14132446986", "-a", "Recording.m4a" ])

os.chdir(origWD) # get back to our original working directory

