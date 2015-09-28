# pydarkstar

A python module and set of command line tools for interacting with a darkstar server.

# Quickstart

This is a quick giude to getting pydarkstar running.  For more detail, as well as understanding how pydarkstar works, **please read the usage section**.

#### LINUX

* Linux already comes with python.  **You should use python3**, which is not the default.

```bash
bash:~$ sudo apt-get install git
bash:~$ sudo apt-get install pip

bash:~$ sudo pip install sqlalchemy
bash:~$ sudo pip install pymysql
bash:~$ sudo pip install beautifulsoup4
bash:~$ sudo pip install pyyaml

bash:~$ git clone git@github.com:AdamGagorik/pydarkstar.git

# enter the correct path!
bash:~$ cd ./path/to/pydarkstar
bash:~$ python3 ./makebin.py
```

**Edit the config.yaml in "C:\path\to\pydarkstar\bin" with your settings (use a text editor).**

```bash
bash:~$ cd /path/to/pydarkstar/bin

# to download new data from ffxiah.com (takes forever)
bash:~$ ./scrub.sh

# to start the broker
bash:~$ ./broker.sh
```

#### WINDOWS

* Setting up Python on Windows can be painful if you are not familiar with shell scripting, PATH variables, etc.
* It may be easier to install a Python distribution such as Anaconda (http://continuum.io/downloads).

---

* Install Git

**You have it already, if you are running darkstar.**

* Install Python Anaconda

**Really, its the easiest way.**

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
**Search for it using the start menu.**

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

# Features
* create prices database
* human editable price database
* populate auction house with prices
* buy items put up for sale by players

# Requires
* python 3.4.3
* sqlalchemy 1.0.8
* pymysql 0.6.6
* bs4 4.3.2
* pyyaml 3.11

**The requirements can be installed using pip or Anaconda, however, there are many other ways**

```bash
pip install sqlalchemy
pip install pymysql
pip install beautifulsoup4
pip install pyyaml
```

# Download

```bash
git clone git@github.com:AdamGagorik/pydarkstar.git
```

# Usage

* Use pydarkstar from the command line.

```bash
C:\path\to\pydarkstar\bin> .\broker.bat
```

* There are many apps...

| app    | description                                                         |
|--------|---------------------------------------------------------------------|
| scrub  | download data from the web to create a database of items and prices |
| broker | server that buys and sells items on the AH from players             |
| buyer  | server that buys items on the AH from players                       |
| seller | server that sells items on the AH to players                        |
| clear  | clear the AH of all transactions                                    |
| refill | fill the AH with items for sale and exit                            |
| alter  | alter the item database                                             |

* **Configure the apps by passing command line arguments**
* **Or, setting parameters in the config.yaml file**
* Please do not edit source code files to configure your apps.
* You can change many properties be editing the item database (items.csv).

| column   | description             | value          |
| ---------|-------------------------|----------------|
| itemid   | unique item id          | integer        |
| name     | item name               | string         |
| sell01   | sell single?            | 0=false 1=true |
| buy01    | buy single?             | 0=false 1=true |
| price01  | price for single        | integer >=1    |
| stock01  | restock count (single)  | integer >=0    |
| sell12   | sell stack?             | 0=false 1=true |
| buy12    | buy stack?              | 0=false 1=true |
| price12  | price for stack         | integer >=1    |
| stock12  | restock count (stack)   | integer >=0    |

# Advanced

#### Setting the PYTHONPATH

**The pydarkstar package will not work unless you tell python where pydarkstar is located**.

*This is just how python works, and is not here to make things complicated.*

We accomplish this by writing shell scripts that set an environment variable called PYTHONPATH to the absolute path of the pydarkstar root directory.  Running the included makebin.py sets this up automatically for you.  Below are example scripts, should you want to perform this setup process manually.

###### LINUX

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

###### WINDOWS

* Create the following text file.
* Please note that spaces in directory names can cause issues to arise when quotes are not used.

```bat
@ECHO OFF
set PYTHONPATH="%PYTHONPATH%;C:\Path\To\pydarkstar"
python3 -m pydarkstar.apps.scrub.run %*
```

###### I DON'T CARE

You can forget about all this PYTHONPATH stuff if your terminal is at the pydarkstar root directory when executing apps.
```bash
bash:~$ cd /path/to/pydarkstar
```

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
