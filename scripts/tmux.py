#!/usr/bin/env python
import os
import subprocess
import sys

print("TMUX: %s" % os.getenv("TMUX", ""))
print("SSH_TTY: %s" % os.getenv("SSH_TTY", ""))
print("SSH_AUTH_SOCK: %s" % os.getenv("SSH_AUTH_SOCK", ""))
print("HOME: %s" % os.getenv("HOME", ""))

session_name  = 'default'
if len(sys.argv) > 1:
    session_name = sys.argv[1]

ssh_auth_sock = '-'.join(['ssh_auth_sock', os.getenv('HOSTNAME'), session_name])

if os.getenv("TMUX") is None:
    if os.getenv("SSH_TTY") is not None:
        if os.getenv("SSH_AUTH_SOCK") is not None:
            sock_file = os.path.join(os.getenv("HOME"), '.ssh', ssh_auth_sock)
            try:
                #always try to remove
                os.remove(sock_file)
            except OSError:
                pass
            os.symlink(os.getenv("SSH_AUTH_SOCK"), sock_file)
            os.environ['SSH_AUTH_SOCK'] = sock_file

    try:
        subprocess.check_call(["tmux", "attach-session", "-t", session_name])
    except subprocess.CalledProcessError:
        print("lets create session")
        os.environ['STY'] = "tmux-sshwrap"
        os.execlpe("tmux", "tmux", "new-session", "-s", session_name,
                   os.environ)
