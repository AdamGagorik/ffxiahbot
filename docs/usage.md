# Config

You must create a YAML file to configure the tool.
All other options are passed as command line arguments.

```yaml
# ah
name: Zissou # Name that appears on AH when buying and selling
tick: 30 # seconds between buying
restock: 3600 # seconds between selling

# sql
hostname: 127.0.0.1 # SQL parameter
database: dspdb # SQL parameter
username: root # SQL parameter
password: ???? # SQL parameter
fail: true # fail on SQL database errors?
```

# Usage

Simply run the `ffxiahbot` from the command line.
Specify the app you want to run and any flags you want to set.

```{warning}
Common command line flags like --verbose must come before the name of the app to run.
App specific command line flags must come after the name of the app to run.
```

```bash
➜  ffxiahbot --help

 Usage: ffxiahbot [OPTIONS] COMMAND [ARGS]...

 The script will interact with the Auction House of a private Final Fantasy XI server.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version                      Also show DEBUG messages.                                                                                       │
│ --silent                       Only show ERROR messages.                                                                                       │
│ --verbose                      Enable verbose logging.                                                                                         │
│ --logfile                PATH  The path to the log file. [default: ahbot.log]                                                                  │
│ --disable-logfile              Disable logging to a file.                                                                                      │
│ --help                         Show this message and exit.                                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ broker   Run a bot that buys and sells items on the auction house continuously.                                                                │
│ clear    Delete items from the auction house (dangerous operation!).                                                                           │
│ refill   Refill the auction house with the items defined in the CSV file.                                                                      │
│ scrub    Download a list of item prices from ffxiah.com and save to a CSV file.                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Download Items CSV

This command will download item data from ffxiah.com and save it to a CSV file.

```bash
➜  ffxiahbot --verbose scrub
➜  ffxiahbot --verbose scrub --server ASURA
➜  ffxiahbot --verbose scrub --item-id 1 --item-id 2 --item-id 3
➜  ffxiahbot --verbose scrub --cat-url http://www.ffxiah.com/browse/62/grips
```

```{important}
There is a pre-built CSV file in the repo, so you do not need to run this command if you don't want to.
```

```bash
➜  ffxiahbot scrub --help

 Usage: ffxiahbot scrub [OPTIONS]

 Download a list of item prices from ffxiah.com and save to a CSV file.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --config              PATH                                                        Config file path. [default: config.yaml]                     │
│ --out-csv             PATH                                                        The output CSV file to save. [default: items.csv]            │
│ --server              [BAHAMUT|SHIVA|TITAN|RAMUH|PHOENIX|CARBUNCLE|FENRIR|SYLPH|  The server ID to scrub. [default: ASURA]                     │
│                       VALEFOR|ALEXANDER|LEVIATHAN|ODIN|IFRIT|DIABOLOS|CAITSITH|Q                                                               │
│                       UETZALCOATL|SIREN|UNICORN|GILGAMESH|RAGNAROK|PANDEMONIUM|G                                                               │
│                       ARUDA|CERBERUS|KUJATA|BISMARCK|SERAPH|LAKSHMI|ASURA|MIDGAR                                                               │
│                       DSORMR|FAIRY|REMORA|HADES]                                                                                               │
│ --cat-url             TEXT                                                        Preset category URLs.                                        │
│ --item-id             INTEGER                                                     Preset item IDs.                                             │
│ --overwrite                                                                       Overwrite output CSV?                                        │
│ --stock-single        INTEGER                                                     The default number of items for singles. [default: 10]       │
│ --stock-stacks        INTEGER                                                     The default number of items for stacks. [default: 10]        │
│ --backup                                                                          Backup output CSV?                                           │
│ --help                                                                            Show this message and exit.                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Refill AH

```{important}
Run the `refill` app to populate the AH if you want to buy items immediately!
```

```bash
➜  ffxiahbot refill
```

```bash
➜  ffxiahbot refill --help

 Usage: ffxiahbot refill [OPTIONS]

 Refill the auction house with the items defined in the CSV file.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --config           PATH  Config file path. [default: config.yaml]                                                                              │
│ --inp-csv          PATH  Input CSV file path. [default: items.csv]                                                                             │
│ --no-prompt              Do not ask for confirmation.                                                                                          │
│ --help                   Show this message and exit.                                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Run AH Bot

```bash
➜  ffxiahbot broker
```

```{warning}
The `broker` will wait until the 1st cycle defined in your config before populating items.
```

```bash
➜  ffxiahbot broker --help

 Usage: ffxiahbot broker [OPTIONS]

 Run a bot that buys and sells items on the auction house continuously.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --config                           PATH  Config file path. [default: config.yaml]                                                              │
│ --inp-csv                          PATH  Input CSV file path. [default: items.csv]                                                             │
│ --buy-items     --no-buy-items           Enable the buying of items. [default: buy-items]                                                      │
│ --sell-items    --no-sell-items          Enable the selling of items. [default: sell-items]                                                    │
│ --help                                   Show this message and exit.                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Item Database

- Item data is stored in _items.csv_
- _items.csv_ is just a simple text file that you can edit with excel
- The _items.csv_ can be created with the scrub app
- There is an already generated _items.csv_ in the bin folder for you
- You do not need to run the _scrub_ app unless you want to recreate the database
- You can change many properties be editing the _items.csv._ manually
- You can change the FFXI `--server` that is used to download info from

```{warning}
You do not need to regenerate it even if you think it is old! You can cause yourself pricing issues, you have been warned!
```

```{warning}
There is no reason to run the scrub app as an `items.csv` is included already in the repository!
```

```{warning}
Retail sometimes has unexpected prices in the history.

  * There may be ancient entries.
  * Something might be sold something below NPC price.
  * An item may only really sell as either a stack or a single.

This may result in exploits on your server if you are not careful.
```

| column       | description                    | value             |
| ------------ | ------------------------------ | ----------------- |
| itemid       | unique item id                 | integer >=0       |
| name         | item name                      | string            |
| sell_single  | sell single?                   | 0=false 1=true    |
| buy_single   | buy single?                    | 0=false 1=true    |
| price_single | price for single               | integer >=1       |
| stock_single | restock count (single)         | integer >=0       |
| rate_single  | buy rate (single) **not used** | float 0 <= x <= 1 |
| sell_stacks  | sell stack?                    | 0=false 1=true    |
| buy_stacks   | buy stack?                     | 0=false 1=true    |
| price_stacks | price for stack                | integer >=1       |
| stock_stacks | restock count (stack)          | integer >=0       |
| rate_stacks  | buy rate (stack) **not used**  | float 0 <= x <= 1 |
