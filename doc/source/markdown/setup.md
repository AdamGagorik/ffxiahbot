# Setup

This is a giude to getting pydarkstar running.

# Step 0: Install Git and Clone pydarkstar

* You installed **git** already when you setup [darkstar][DARKS]
* Clone the pydarkstar repository from [here][GITPG]

# Step 1: Install Python

**GOTCHA**:  Make sure you use **Python version 3**!

### Choice 1: Anaconda (Recommended)

* Install [Python Anaconda][CONDA]
* You need **Python3.4** or greater.

### Choice 2: Use Your OS's Python (Linux ONLY)

* Linux already comes with python installed
* You need **Python3.4** or greater (may not be the default)

### Choice 3: Install Python from Somewhere Else

* You can use the official Python from [here][PYOFF].
* You need **Python3.4** or greater.

# Step 2: Install 3rd-party Python Modules

### Choice 1:  Use Anaconda's Conda Command (Recommended)

* **GOTCHA**: You must have installed Anaconda above!
* **GOTCHA**: Use the Anaconda Command Prompt on **WINDOWS** (search for it in the start menu)

Open a command prompt and run the following commands:

```bash
conda update conda

# when prompted, enter 'y' for yes

conda install sqlalchemy
conda install pymysql
conda install beautiful-soup
conda install pyyaml
conda install six
```

### Choice 2:  Use Pip

* **GOTCHA**: Make sure you have the **pip** command!
* **GOTCHA**: Notice that its beautifulsoup4 instead of beautiful-soup

Open a command prompt and run the following commands:

###### Windows

```bash
"C:\path\to\pip" install sqlalchemy
"C:\path\to\pip" install pymysql
"C:\path\to\pip" install beautifulsoup4
"C:\path\to\pip" install pyyaml
"C:\path\to\pip" install six
```

###### Linux

```bash
sudo pip install sqlalchemy
sudo pip install pymysql
sudo pip install beautifulsoup4
sudo pip install pyyaml
sudo pip install six
```

# Step 4: Configure pydarkstar

Follow the instructions on the [usage][USAGE] page.

[CONDA]: http://continuum.io/downloads
[PYPIP]: https://pip.pypa.io/en/stable/
[PYOFF]: https://www.python.org/downloads
[USAGE]: http://adamgagorik.github.io/pydarkstar/generated/usage.html
[GITPG]: https://github.com/AdamGagorik/pydarkstar
[DARKS]: https://github.com/DarkstarProject/darkstar