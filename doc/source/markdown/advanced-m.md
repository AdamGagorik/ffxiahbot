#### Running Apps

**Please note that pydarkstar takes advantage of python's -m flag to run library modules as scripts**.  Python modules are just python files beneath the pydarkstar top level directory.  There is no other way to run the apps.

###### THIS WILL WORK

```bash
bash:~$ cd /path/to/pydarkstar
bash:~$ python3 -m pydarkstar.apps.scrub.run --help
```

######  THIS WILL NOT WORK

```bash
bash:~$ cd /path/to/pydarkstar
bash:~$ python3 ./pydarkstar/apps/scrub/run.py --help
```