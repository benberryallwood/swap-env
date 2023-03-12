# Swap Env

`swap-env` is a simple CLI for swapping between different `.env` files.

## Installation

- with [`pipx`](https://pypa.github.io/pipx/) (recommended):

```bash
pipx install swap-env
```

- with `pip`:

```bash
pip install swap-env
```

## Usage

Save any `.env` files you regularly use to `~/.swap-env/`. Name them `.env.<name>` and you'll access them via `<name>` in `swap-env`.
Then simply run `swap-env` and select the file you want to use. A symlink will be created at `./.env` to that file.

**Note:** This will overwrite any file or link currently at `./.env`
