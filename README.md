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

# Usage

* **option 1**
 The main scripts are located in ./path/to/pydarkstar/apps.
 They should work if run *from that directory*.

 ```bash
 cd ./path/to/pydarkstar/apps
 python ./scrub.py --help
 ```

*To run the script from another directory, you must tell python where the pydarkstar module is.*

* **option 2** : add to PYTHONPATH temporarily

 ```bash
 export PYTHONPATH=$PYTHONPATH:/path/to/pydarkstar/
 ```

* **option 3** : add to PYTHONPATH permanently, on Linux

 ```bash
 echo "PYTHONPATH=$PYTHONPATH:/path/to/pydarkstar/" >> ~/.bashrc
 source ~/.bashrc
 ```

* **option 4** : install module

 ```bash
 cd ./path/to/pydarkstar/
 python setup.py
 ```

*If using options 2, 3, or 4, you can run apps from anywhere.*

 ```bash
 cd /somewhere/else
 python ./path/to/pydarkstar/apps/scrub.py
 ```

# Apps

###### scrub

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

###### broker

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

###### alter

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

# Tests
Tests are in ./path/to/pydarkstar/tests
