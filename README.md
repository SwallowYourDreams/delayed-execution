# delayed-execution
This script allows the user to delay the execution of a command, e.g. to shut down their machine after a set amount of time.

##FAQ

**Why not just use 'sleep 1h; your_command'?**

This script is geared towards users who have little to no experience with the command line. Novice users can use the GUI to simply delay tasks on their machine.

**Which OSs are supported?**

This script will only work on Linux machines.

**Which Linux distributions are supported?**

The script was written for and tested on Ubuntu and derivatives such as Linux Mint. Most of the built-in commands (such as shutdown or reboot) are universal for all distributions. "Suspend", however, may be different for your distribution and may require you to pass your distribution-specific suspend command using the -c option.
