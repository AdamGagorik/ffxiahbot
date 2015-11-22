# Advanced

#### Shell Scripts : PYTHONPATH

**The pydarkstar package will not work unless you tell python where pydarkstar is located**.

*This is just how python works, and is not here to make things complicated.*

We accomplish this by writing shell scripts that set an environment variable called PYTHONPATH to the absolute path of the pydarkstar root directory.  **Running the included makebin.py sets this up automatically for you**.  Below are example scripts, should you want to perform this setup process manually.

The process of setting the PYTHONPATH is not needed in the case that pydarkstar is in the current directory of an executing python interpreter.

##### Linux

* Create the following text file.

```bash
#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/path/to/pydarkstar
python3 -m pydarkstar.apps.scrub.run $*
```

* Make the file executable.

```bash
bash:~$ chmod +x scrub.sh
```

* Run the app.

```bash
bash:~$ ./scrub.sh --help
```

##### Windows

* Create the following text file.
* Please note that spaces in directory names can cause issues to arise when quotes are not used.

```bat
@ECHO OFF
set PYTHONPATH="%PYTHONPATH%;C:\Path\To\pydarkstar"
python3 -m pydarkstar.apps.scrub.run %*
```

#### Shell Scripts : Running Apps

**Please note that pydarkstar takes advantage of python's -m flag to run library modules as scripts**.  Python modules are just python files beneath the pydarkstar top level directory.  There is no other way to run the apps.

* This will work

```bash
bash:~$ cd /path/to/pydarkstar
bash:~$ python3 -m pydarkstar.apps.scrub.run --help
```

* This will not work

```bash
bash:~$ cd /path/to/pydarkstar
bash:~$ python3 ./pydarkstar/apps/scrub/run.py --help
```
