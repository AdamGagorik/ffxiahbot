# pydarkstar

A python module for interacting with a darkstar server.

# Features
* create prices database
* human editable price database
* populate auction house with prices
* buy items put up for sale by players

# Requires
* python 2.7.8
* sqlalchemy 0.9.8
* pymysql 0.6.2
* bs4 4.3.2
* pyyaml 3.11

*The requirements can be installed using pip, however, there are many other ways*

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

They main scripts, located in ./path/to/pydarkstar/apps, **will not work** unless you do one of the following:

## option 1

Create shell scripts (using the included makebin.py)

###### LINUX

```bash
cd ./path/to/pydarkstar/
python ./makebin.py
```

###### WINDOWS

```bash
cd .\path\to\pydarkstar\
python .\makebin.py
```

## option 2

Create shell scripts *manually*.
Create the following using a txt editor, **with the correct paths**:

###### LINUX

Create scrub.sh

```bash
#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/path/to/pydarkstar
python /path/to/pydarkstar/apps/scrub.py $*
```

```bash
chmod +x scrub.sh
```
 
###### WINDOWS

Create scrub.bat

```bash
@ECHO OFF
set PYTHONPATH=%PYTHONPATH%;C:\Path\To\pydarkstar
python C:\Path\To\pydarkstar\apps\scrub.py %*
```

## option 3

Add to PYTHONPATH temporarily, before calling a script.

###### LINUX

```bash
cd ./path/to/pydarkstar/
export PYTHONPATH=$PYTHONPATH:/path/to/pydarkstar/
python ./scrub.py --help
```

###### WINDOWS

```bash
cd C:\Path\To\pydarkstar\apps
set PYTHONPATH=%PYTHONPATH%;C:\Path\To\pydarkstar
python .\scrub.py --help
```

## option 4

Add to PYTHONPATH permanently.

###### LINUX

```bash
echo "PYTHONPATH=$PYTHONPATH:/path/to/pydarkstar/" >> ~/.bashrc
source ~/.bashrc
```

###### WINDOWS

Edit your environment variables using the control panel, setting the PYTHONPATH.

## option 5

Install module.

###### LINUX

```bash
cd ./path/to/pydarkstar/
python setup.py
```

# Apps

* The apps can be configured using command line flags or configuration files.
* The priority of arguments is *defaults < config < command line*
* Each app has a **--save** command line argument that will create a default configuration file.

#### scrub

This script creates an item database in the form of a simple CSV text file.
That text file can be used by *broker.py* to stock the auction house as
well as buy items sold by players.

The script:
  1.  downloads a list of category urls
    * **this information is saved and reused** (override reuse with *--force*)
  2.  extracts item ids from category urls
    * **this information is saved and reused** (override reuse with *--force*)
  3.  downloads price information for each item id
  4.  saves the information in a CSV file

```bash
python ./path/to/pydarkstar/apps/scrub.py --help

usage: scrub.py [-h] [--verbose] [--silent] [--overwrite] [--backup] [--save]
                [--force] [--threads -1] [--urls [url [url ...]]]
                [--itemids [itemids [itemids ...]]] [--stock01 5]
                [--stock12 5]
                [stub]

Create item database.

positional arguments:
  stub                  output file stub

optional arguments:
  -h, --help            show this help message and exit
  --verbose             report debug, info, and error
  --silent              report error only
  --overwrite           overwrite output file
  --backup              backup output file
  --save                save config file (and exit)
  --force               start from scratch
  --threads -1          number of cpu threads to use
  --urls [url [url ...]]
                        a list of category urls
  --itemids [itemids [itemids ...]]
                        a list of item ids
  --stock01 5           default stock for singles
  --stock12 5           default stock for stacks
```

###### examples

```
# basic usage
python scrub.py --force 
```

#### broker

This script runs like a server, looking for items that people put up for auction.
The items are then bought and restocked.  Information on prices is read from
a simple CSV text file that can be created with *scrub.py*.

The script:
  1.  loads item data (from text file created by scrub.py)
  2.  populates AH with items and exits (if using **--refill**)
  3.  buys items from player every **tick** seconds
  4.  restocks items every **restock** seconds

```bash
python ./path/to/pydarkstar/apps/broker.py --help

usage: broker.py [-h] [--verbose] [--silent] [--find] [--save]
                 [--hostname str] [--database str] [--username str]
                 [--password str] [--fail] [--clear] [--all] [--force]
                 [--name str] [--restock int] [--refill] [--tick int]
                 [str [str ...]]

Buy and sell items on the auction house.

positional arguments:
  str             item data CSV file(s)

optional arguments:
  -h, --help      show this help message and exit
  --verbose       report debug, info, and error
  --silent        report error only
  --find          search for item data files
  --save          save config file (and exit)
  --hostname str  SQL address
  --database str  SQL database
  --username str  SQL username
  --password str  SQL password
  --fail          fail on SQL errors
  --clear         clear items sold by seller
  --all           clear *all* items
  --force         clear *all* items
  --name str      seller name
  --restock int   restock interval in seconds
  --refill        restock items at start and exit
  --tick int      buying interval in seconds
```

###### examples

```
# basic usage
python broker.py items.csv
```

#### alter

This script is meant for altering the item CSV database from the command line,
if one perfers.  However a text editor or excel can accomplish the same task.
**The functionality of alter.py has not yet been implemented.**

```bash
python ./path/to/pydarkstar/apps/alter.py --help

usage: alter.py [-h] [--verbose] [--silent] [--overwrite] [--backup] [--save]
                [--show] [--all] [--lambda lambda : True] [--match .*]
                [--itemids [itemids [itemids ...]]] [--create] [--reset]
                [--scrub] [--set key=value] [--execute]
                [ifile] [ofile]

Alter item database.

positional arguments:
  ifile                 output file stub
  ofile                 output file stub

optional arguments:
  -h, --help            show this help message and exit
  --verbose             report debug, info, and error
  --silent              report error only
  --overwrite           overwrite output file
  --backup              backup output file
  --save                save config file (and exit)
  --show                show itemids and exit
  --all                 select all itemids
  --lambda lambda : True
                        select itemids where lambda evaluates to True
  --match .*            select itemids where name matches regex
  --itemids [itemids [itemids ...]]
                        a list of item ids
  --create              create a new item (if it doesnt exist)
  --reset               reset columns to defaults for item
  --scrub               redownload data for item
  --set key=value       set column to value for item
  --execute             actually run commands (default mode is a dry run)
```

###### examples

```
# basic usage
python alter.py --help 
```
