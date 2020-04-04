# delayed-execution
This script allows the user to delay the execution of a command, e.g. to shut down their machine after a set amount of time.

## Dependencies

* PyQt5

## FAQ

**Why not just use 'sleep 1h; your_command'?**

This script is geared towards users who have little to no experience with the command line. Novice users can use the GUI to simply delay tasks on their machine.

**Which operating systems are supported?**

Parts of this script (such as shutdown and reboot) should run on all Unix-based operating systems,such as the various Linux and BSD distributions as well as MacOS. Windows is not supported.

The "suspend" option will only work on systems running systemd (such as Ubuntu, Debian, Fedora, Arch Linux, Manjaro, etc). If yours is a non-systemd distribution, you may work around this by running the command "sudo pm-suspend". A similar suspend workaround goes for MacOS users, who must run the command "pmset sleepnow".
