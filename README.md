AP_REBOOT.py
I have found that I needed to reboot all of my aps a couple of times due to some issues with authentication changes on the back end. Instead of having to click through them one by one I decided to build a script that would either go through and reboot them all as fast was possible or go on a timed interval so that the whole network didn't go down at once. This is the result of that script and what I put together for it. The script is fairly simple in what it does, it presents a list of networks in the org and then you type in the one you would like to go through and do reboots on.