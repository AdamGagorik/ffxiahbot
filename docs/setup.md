# Setup

### Step 1: Install [uv][uv]

```bash
# Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: Run the app

```bash
git clone https://github.com/AdamGagorik/ffxiahbot.git
cd ffxiahbot/bin
uv run ffxiahbot --help
```

### Step 3: Configure the bot

Follow the instructions on the [usage][USAGE] page.

[uv]: https://docs.astral.sh/uv
[USAGE]: http://adamgagorik.github.io/ffxiahbot/usage
