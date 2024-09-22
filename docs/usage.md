# Usage

## TLDR

Edit the `config.yaml` and `items.csv` files in the `bin` folder.

- [`config.yaml`](https://github.com/AdamGagorik/ffxiahbot/blob/master/bin/config.yaml)
- [`items.csv`](https://github.com/AdamGagorik/ffxiahbot/blob/master/bin/items.csv)

From the `bin` folder, run any of the following commands:

```bash
uv run ffxiahbot broker
uv run ffxiahbot clear
uv run ffxiahbot refill
uv run ffxiahbot scrub
```

!!! important

    Run the `ffxiahbot` command inside a directory that contains a `config.yaml` and optionally an `items.csv`.

!!! warning

    The way you run the ffxiahbot command depends on how you installed it.

    | Installation Method | Command                   |
    |---------------------|---------------------------|
    | uv                  | `uv run ffxiahbot --help` |
    | pipx                |        `ffxiahbot --help` |

## Creating the Config File

You must create a YAML file to configure the tool (`config.yaml`). All other
options are passed as command line arguments.

```yaml
# ah
name: M.H.M.U. # Name that appears on AH when buying and selling
tick: 30 # seconds between buying
restock: 3600 # seconds between selling

# sql
hostname: 127.0.0.1 # SQL parameter
database: xidb # SQL parameter
username: root # SQL parameter
password: root # SQL parameter
port: 3306 # SQL parameter
fail: true # fail on SQL database errors?
```

## Running the CLI

Simply run the `ffxiahbot` from the command line. Specify the app you want to
run and any flags you want to set.

!!! warning

    Common command line flags like --verbose must come before the name of the app to run.
    App specific command line flags must come after the name of the app to run.

{{ get_help_message("ffxiahbot") }}

#### Downloading a new Items CSV

This command will download item data from ffxiah.com and save it to a CSV file.

```bash
➜  uv run ffxiahbot --verbose scrub
➜  uv run ffxiahbot --verbose scrub --server ASURA
➜  uv run ffxiahbot --verbose scrub --item-id 1 --item-id 2 --item-id 3
➜  uv run ffxiahbot --verbose scrub --cat-url http://www.ffxiah.com/browse/62/grips
```

!!! important

    There is a pre-built CSV file in the repo, so you do not need to run this command if you don't want to.

{{ get_help_message("ffxiahbot", "scrub") }}

#### Refilling the Auction House

!!! important

    Run the `refill` app to populate the AH if you want to buy items immediately!

```bash
➜  uv run ffxiahbot refill --inp-csv items.csv
```

{{ get_help_message("ffxiahbot", "refill") }}

#### Clearing the Auction House

This command will remove all items for sale from the AH.

!!! warning

    This command is pretty destructive, so be careful!

!!! important

    Unless `--all` is specified, this command will only clear items that are for sale by the bot.

{{ get_help_message("ffxiahbot", "clear") }}

#### Running the AH Broker Bot

```bash
➜  uv run ffxiahbot broker --inp-csv items.csv --buy-items --sell-items
```

!!! warning

    The `broker` will wait until the 1st cycle defined in your config before populating items.

{{ get_help_message("ffxiahbot", "broker") }}

#### Manually Editing the Items CSV

- Item data is stored in _items.csv_ (you can edit it with a text editor or
  Excel)
- There is an already generated _items.csv_ in the bin folder for you

!!! warning

    - There is no reason to run the scrub app as an `items.csv` is included already in the repository!
    - You do not need to regenerate the database even if you think it is old!
    - You can cause yourself pricing issues, you have been warned!

!!! warning

    Retail sometimes has unexpected prices in the history.

      * There may be ancient entries.
      * Something might be sold something below NPC price.
      * An item may only really sell as either a stack or a single.

    This may result in exploits on your server if you are not careful.

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
