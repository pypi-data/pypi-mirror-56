#! /usr/bin/python

import fcntl
import os

class FileNotLocked(Exception):
    pass

class FlockFile:

    def unlock(self):
        self.lockfd.close()
        os.remove(self.lock_file)

    def lock(self):

        # if it's a directory, crash
        if os.path.isdir(self.lock_file):
            raise RuntimeError("The lock file path is a directory.")

        # touch the file if it doesn't exist.
        if not os.path.isfile(self.lock_file):
            open(self.lock_file, 'a').close()            

        try:
            self.lockfd = open(self.lock_file, "w")
            fcntl.flock(self.lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.locked = True
        except IOError:
            self.locked = False
            raise FileNotLocked("Unable to obtain lock on {}".format(self.lock_file))


    def __init__(self, file_name, lock_dir="/tmp"):
        
        self.lock_file = os.path.join(lock_dir, file_name)
        self.locked = False
        self.lockfd = None