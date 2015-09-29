# Quickstart

This is a quick giude to getting pydarkstar running.  For more detail, as well as understanding how pydarkstar works, **please read the usage section**.

#### Linux

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

#### Windows

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
> cd "C:\path\to\pydarkstar"
> "C:\path\to\python3" .\makebin.py
```

**Edit the config.yaml in "C:\path\to\pydarkstar\bin" with your settings (use a text editor).**

```bash
> cd "C:\path\to\pydarkstar\bin"

# to download new data from ffxiah.com (takes forever)
> .\scrub.bat

# to start the broker
> .\broker.bat
```
