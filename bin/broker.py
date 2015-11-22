#!/usr/bin/env python
import logging
import sys
import os


try:
    import pydarkstar
except ImportError:
    pydarkstar_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, pydarkstar_path)
    import pydarkstar


import pydarkstar.apps.broker.run
import pydarkstar.logutils


if __name__ == '__main__':
    with pydarkstar.logutils.capture():
        pydarkstar.apps.broker.run.main()
    logging.info('exit\n')
