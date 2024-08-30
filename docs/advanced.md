# Advanced

Here are some alternative ways to install `ffxiahbot` if you are familiar with Python and its package management tools.

## Installation using uv

```bash
uvx ffxiahbot --help
```

## Installation using pipx

```bash
pipx install ffxiahbot
ffxiahbot --help
```

## Installation into a virtual environment (pyenv + pip)

```bash
pyenv install 3.12
pyenv local 3.12
pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install ffxiahbot
ffxiahbot --help
```

## Run from source

```bash
git clone https://github.com/AdamGagorik/pydarkstar.git
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
source venv/bin/activate
python -m ffxiahbot --help
```
