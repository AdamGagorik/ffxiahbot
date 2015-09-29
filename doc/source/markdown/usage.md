# Usage

#### Basic

* Use pydarkstar from the command line.

```bash
C:\path\to\pydarkstar\bin> .\broker.bat
```

* Use the --help flag for a list of options.

```bash
C:\path\to\pydarkstar\bin> .\broker.bat --help
```

#### Apps

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

#### Parameters

* **Configure the apps by passing command line arguments.**
* **Parameters can also be set in the config.yaml file.**
* The order of precedence is *defaults < config file < command line*.
* Please do not edit source code files to configure your apps.
* You should set your mysql parameters.

#### Item Database

* Item data is stored in *items.csv*.
* You can change many properties be editing the item database: *items.csv.*

| column   | description             | value          |
| ---------|-------------------------|----------------|
| itemid   | unique item id          | integer >=0    |
| name     | item name               | string         |
| sell01   | sell single?            | 0=false 1=true |
| buy01    | buy single?             | 0=false 1=true |
| price01  | price for single        | integer >=1    |
| stock01  | restock count (single)  | integer >=0    |
| sell12   | sell stack?             | 0=false 1=true |
| buy12    | buy stack?              | 0=false 1=true |
| price12  | price for stack         | integer >=1    |
| stock12  | restock count (stack)   | integer >=0    |

* There is an already generated *items.csv* in the bin folder for you.
* You do not need to run the *scrub* app unless you want to recreate the database.
