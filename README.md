# oreo-Hack.Lu-CTF-2014-
ctf writeup for oreo.

Head over to https://github.com/ctfs/write-ups-2014/blob/master/hack-lu-ctf-2014/oreo/README.md, or download the "oreo" file uploaded here and get the binary if you want to try.

Overwrites the sscanf pointer, so exit() in spawned shell loops back to another shell. To exit, use kill [pid], (pid printed on execution).

Will post a brief analysis on https://testzer0.wixsite.com/mysite soon.

sploit1.py is the exploit. It uses values hardcoded for my system, may be different on yours. Make appropriate changes before using.
