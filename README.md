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

Execute `run.sh` in a terminal. It will prompt you for your superuser password and pass these privileges on to the actual script. This is necessary for running commands that require superuser privileges, such as shutdown and reboot.

**Why doesn't my machine power off / reboot / suspend?**

Please note that shutdown and reboot require superuser privileges. These must be obtained by running the script as root: `sudo DelayedExecution.py`. The file `run.sh` does just that, so just start the script through `run.sh`. Otherwise the script will prompt you to enter the superuser password _after_ the countdown has ended, which is probably not useful.
