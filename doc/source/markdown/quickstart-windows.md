#### WINDOWS

* Setting up Python on Windows can be painful.
* It is easier to install a Python distribution such as Anaconda (http://continuum.io/downloads).

* Install Git
* Install Python Anaconda
* Open the Anaconda command prompt from the start menu

**Search for it using the start menu**

```bash
> conda update conda

# when prompted, enter 'y' for yes

> conda install sqlalchemy
> conda install pymysql
> conda install beautiful-soup
> conda install pyyaml
```

* Clone pydarkstar repository
* Run the makebin.py script

**You need to open a command prompt at the root directory of pydarkstar.**

```bash
# enter the correct path!
C:\Users\Steve> cd "C:\path\to\pydarkstar"
C:\path\to\pydarkstar> "C:\path\to\python3" .\makebin.py
```

**Edit the config.yaml in "C:\path\to\pydarkstar\bin" with your settings (use a text editor).**

```bash
C:\Users\Steve> cd "C:\path\to\pydarkstar\bin"

# to download new data from ffxiah.com (takes forever)
C:\path\to\pydarkstar> .\scrub.bat

# to start the broker
C:\path\to\pydarkstar> .\broker.bat
```