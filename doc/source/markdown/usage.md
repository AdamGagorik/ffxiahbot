# Usage

#### Example

```bash
# Windows

> cd /D "C:\path\to\pydarkstar\bin"
> conda activate pydarkstar
> .\refill.py
> .\broker.py

# Linux

bash:~$ cd /path/to/pydarkstar/bin
bash:~$ conda activate pydarkstar
bash:~$ ./refill.py
bash:~$ ./broker.py
```

```{warning}
The `broker` will wait until the 1st cycle defined in your config before populating items.
```

```{important}
Run the `refill` app to populate the AH if you want to buy items immediately!
```

#### Parameters

* You should set your mysql parameters!
* Parameters can be set in the config.yaml file
* You can also override parameters on the command line
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
server: bahamut       # FFXI server to query
threads: -1           # number of CPU threads
itemids: []           # list of itemids to scrub
stock_single: 10      # default stock_single when scrubbing
stock_stacks: 10      # default stock_stacks when scrubbing
urls: []              # list of category urls to scrub
```

#### Item Database

Item data is stored in a **CSV** file called *items.csv*. This is just a simple text file that you can edit with excel.
Please see the [scrubbing](./scrubbing.md) guide info on how this is generated. 
**You do not need to regenerate it even if you think it is old! You can cause yourself pricing issues, you have been warned!**

| column       | description                     | value             |
| -------------|---------------------------------|-------------------|
| itemid       | unique item id                  | integer >=0       |
| name         | item name                       | string            |
| sell_single  | sell single?                    | 0=false 1=true    |
| buy_single   | buy single?                     | 0=false 1=true    |
| price_single | price for single                | integer >=1       |
| stock_single | restock count (single)          | integer >=0       |
| rate_single  | buy rate (single) **not used**  | float 0 <= x <= 1 |
| sell_stacks  | sell stack?                     | 0=false 1=true    |
| buy_stacks   | buy stack?                      | 0=false 1=true    |
| price_stacks | price for stack                 | integer >=1       |
| stock_stacks | restock count (stack)           | integer >=0       |
| rate_stacks  | buy rate (stack) **not used**   | float 0 <= x <= 1 |

#### Apps

```{warning}
There is no need to run the scrub app as an `items.csv` is included already!
```

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
