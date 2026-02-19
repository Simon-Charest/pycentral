from os import O_WRONLY, close, devnull, dup, dup2, open
from sys import stderr


def mute(fd: int = -1) -> int:
    fd2: int = stderr.fileno()
    fd_dupe: int
    
    if fd > -1:
        dup2(fd, fd2)
        fd_dupe = -1

    else:
        fd = open(devnull, O_WRONLY)
        dup2(fd, fd2)
        fd_dupe = dup(fd)
        close(fd)

    return fd_dupe
