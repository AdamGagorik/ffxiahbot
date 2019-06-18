# Usage

#### Example

```bash
# Windows

> cd /D "C:\path\to\pydarkstar\bin"
> conda activate pydarkstar
> .\broker.py

# Linux

bash:~$ cd /path/to/pydarkstar/bin
bash:~$ conda activate pydarkstar
bash:~$ ./broker.py
```

#### Parameters

* Parameters can be set in the config.yaml file
* You should set your mysql parameters
* Please do not edit source code files to configure your apps

###### Example

```yaml
# ah
name: Zissou          # Name that appears on AH when buying and selling

# basic
verbose: true         # ERROR, INFO, DEBUG in log file
silent: false         # ERROR

# input
data: ['items.csv']   # comma seperated list of CSV files

# output
stub: items           # output name when scrubbing
overwrite: false      # overwrite existing output?
backup: true          # backup existing output?

# sql
hostname: 127.0.0.1   # SQL parameter
database: dspdb       # SQL parameter
username: root        # SQL parameter
password: ????        # SQL parameter
fail: true            # fail on SQL database errors?

# broker/seller
restock: 3600         # seconds between selling

# broker/buyer
tick: 30              # seconds between buying

# scrub
itemids: []           # list of itemids to scrub
stock01: 5            # default stock01 when scrubbing
stock12: 5            # default stock12 when scrubbing
urls: []              # list of category urls to scrub
```

#### Item Database

* Item data is stored in *items.csv*
* *items.csv* is just a simple text file that you can edit with excel
* The *items.csv* can be created with the scrub app
* There is an already generated *items.csv* in the bin folder for you
* You do not need to run the *scrub* app unless you want to recreate the database
* You can change many properties be editing the *items.csv.* manually

| column   | description                     | value             |
| ---------|---------------------------------|-------------------|
| itemid   | unique item id                  | integer >=0       |
| name     | item name                       | string            |
| sell01   | sell single?                    | 0=false 1=true    |
| buy01    | buy single?                     | 0=false 1=true    |
| price01  | price for single                | integer >=1       |
| stock01  | restock count (single)          | integer >=0       |
| rate01   | buy rate (single) **not used**  | float 0 <= x <= 1 |
| sell12   | sell stack?                     | 0=false 1=true    |
| buy12    | buy stack?                      | 0=false 1=true    |
| price12  | price for stack                 | integer >=1       |
| stock12  | restock count (stack)           | integer >=0       |
| rate12   | buy rate (stack) **not used**   | float 0 <= x <= 1 |

#### Apps

* There are many apps
* You will probably only use the broker app

| app    | description                                                         |
|--------|---------------------------------------------------------------------|
| scrub  | download data from the web to create a database of items and prices |
| broker | server that buys and sells items on the AH from players             |
| buyer  | server that buys items on the AH from players                       |
| seller | server that sells items on the AH to players                        |
| clear  | clear the AH of all transactions                                    |
| refill | fill the AH with items for sale and exit                            |
