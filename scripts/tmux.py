#!/usr/bin/env python
import os
import subprocess


def is_valid(key):
    if not key.startswith('PYENV'):
        return True

    if key.endswith('_ROOT'):
        return True

    if key.endswith('_SHELL'):
        return True

    return False


def main():
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
            os.environ['STY'] = "tmux-sshwrap"
            env = {k: os.environ[k] for k in os.environ.keys() if is_valid(k)}
            os.execlpe("tmux", "tmux", "new-session", "-s", "sshwrap", env)
    else:
        print('TMUX var is set...')


if __name__ == '__main__':
    print("TMUX: %s" % os.getenv("TMUX", ""))
    print("SSH_TTY: %s" % os.getenv("SSH_TTY", ""))
    print("SSH_AUTH_SOCK: %s" % os.getenv("SSH_AUTH_SOCK", ""))
    print("HOME: %s" % os.getenv("HOME", ""))

    main()
