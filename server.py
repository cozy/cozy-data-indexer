#!/usr/bin/env python
import os
import sys

current_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.remove(current_directory)
sys.path.insert(0, os.path.join(current_directory, 'cozy-indexer'))

from server import main


if __name__ == "__main__":
    main()
