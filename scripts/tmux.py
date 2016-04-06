#!/usr/bin/env python
import os
import subprocess

print("TMUX: %s" % os.getenv("TMUX", ""))
print("SSH_TTY: %s" % os.getenv("SSH_TTY", ""))
print("SSH_AUTH_SOCK: %s" % os.getenv("SSH_AUTH_SOCK", ""))
print("HOME: %s" % os.getenv("HOME", ""))

if os.getenv("TMUX") is None:
    if os.getenv("SSH_TTY") is not None:
        if os.getenv("SSH_AUTH_SOCK") is not None:
            sock_file = os.path.join(os.getenv("HOME"), ".wrap_auth_sock")
            try:
                #always try to remove
                os.remove(sock_file)
            except OSError:
                pass
            os.symlink(os.getenv("SSH_AUTH_SOCK"), sock_file)
            os.environ['SSH_AUTH_SOCK'] = sock_file

    try:
        subprocess.check_call(["tmux", "attach-session", "-t", "sshwrap"])
    except subprocess.CalledProcessError:
        print("lets create session")
        os.environ['STY'] = "tmux-sshwrap"
        os.execlpe("tmux", "tmux", "new-session", "-s", "sshwrap",
                   os.environ)
