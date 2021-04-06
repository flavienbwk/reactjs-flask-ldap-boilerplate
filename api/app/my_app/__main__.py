# This file allows "my-app" package to be run 
# via `python -m` command line. 
from . import manager

if __name__ == '__main__':
    manager.run()
