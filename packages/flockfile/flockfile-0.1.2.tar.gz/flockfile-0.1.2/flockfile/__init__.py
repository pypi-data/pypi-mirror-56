#! /usr/bin/python

import fcntl
import os

class FileNotLocked(Exception):
    pass

class FlockFile:

    def check_lock(self):
        """ Returns true if locked, false if not """

        if hasattr(self.lockfd, 'read'):
            # is a file type object, return whether or not it is open
            return not self.lockfd.closed

        else:
            return False

    def unlock(self):
        """ unlock and delete the file """

        self.lockfd.close()
        self.lockfd = None

        if self.delete_on_unlock:
            os.remove(self.lock_file)


    def lock(self):
        """ create and lock the file """

        # if it's a directory, crash
        if os.path.isdir(self.lock_file):
            raise RuntimeError("The lock file path is a directory.")

        # touch the file if it doesn't exist.
        if not os.path.isfile(self.lock_file):
            open(self.lock_file, 'a').close()            

        try:
            self.lockfd = open(self.lock_file, "w")
            fcntl.flock(self.lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            raise FileNotLocked("Unable to obtain lock on {}".format(self.lock_file))


    def __init__(self, file_name, lock_dir="/tmp", delete_on_unlock=True):
        
        self.lock_file = os.path.join(lock_dir, file_name)
        self.lockfd = None
        self.delete_on_unlock = delete_on_unlock
