# flockfile

Just a simple python lock file class using file locks.

## Usage

```python
from flockfile import FlockFile, FileNotLocked

# init the class using a file name
# optionally, the directory can be set to something other than /tmp
lock = FlockFile("myscriptname", lock_dir="/tmp")


# lock the file
lock.lock()
# if this is unsuccessful, exception FileNotLocked will be raised.

# the following class method can be used to check lock status
assert lock.check_lock()

# unlock and delete file
lock.unlock()
```

## Questions or Issues?

Please report as a Gitlab issue: https://gitlab.com/rveach/flockfile/issues
