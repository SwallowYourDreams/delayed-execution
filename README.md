# delayed-execution
This script allows the user to delay the execution of a command, e.g. to shut down their machine after a set amount of time.

## Dependencies

* PyQt5

## FAQ

**Why not just use 'sleep 1h; your_command'?**

This script is geared towards users who have little to no experience with the command line. Novice users can use the GUI to simply delay tasks on their machine.

**Which operating systems are supported?**

Parts of this script (such as shutdown and reboot) should run on all Unix-based operating systems, such as the various Linux and BSD distributions, as well as MacOS. Windows is not supported.

The "suspend" option will only work on systems running systemd (such as Ubuntu, Debian, Fedora, Arch Linux, Manjaro, etc). If yours is a non-systemd distribution, you may work around this by running the command `sudo pm-suspend`. A similar suspend workaround exists for MacOS users, who must run the command `pmset sleepnow`.

**How do I run the script properly?**

First, make run.sh and DelayedExecution.py executable:

`chmod +x DelayedExecution.py run.sh`

Then execute run.sh in a terminal. It will prompt you for your superuser password, run the script with superuser privileges and then close down the terminal.

**Why doesn't my machine power off / reboot / suspend?**

Please note that shutdown, suspend and reboot require superuser privileges. These must be obtained by running the script as root: `sudo DelayedExecution.py`. Otherwise it will prompt you to enter the superuser password _after_ the countdown has ended.
