# Swap Env

[![PyPI - Version](https://img.shields.io/pypi/v/swap-env.svg)](https://pypi.python.org/pypi/swap-env)
[![PyPI - License](https://img.shields.io/pypi/l/swap-env.svg)](https://github.com/benberryallwood/swap-env/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swap-env.svg)](https://pypi.python.org/pypi/swap-env)
[![Actions status](https://github.com/benberryallwood/swap-env/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/benberryallwood/swap-env/actions/workflows/ci.yml)

`swap-env` is a simple CLI for swapping between different `.env` files.

![demo](https://user-images.githubusercontent.com/71074961/224817847-828bace2-5ab1-47d9-8ad2-e6a3e47d57f8.gif)

## Requirements

`python >= 3.9`

## Installation

- with [`pipx`](https://pypa.github.io/pipx/) (recommended):

```bash
pipx install swap-env
```

If you use a version of python less than `3.9`, you can provide pipx with a different version to use for this package.
I'd recommend [pyenv](https://github.com/pyenv/pyenv) for managing python versions:

```bash
# make sure you have python3.9 installed
pyenv install 3.9

# use that version with pipx
pipx install --python $(pyenv which python3.9) swap-env
```

- with `pip`:

```bash
pip install swap-env
```

## Usage

Save any `.env` files you regularly use to a directory called `.swap-env/`.
This can be in any parent directory of where you want to use it, or in your home directory.
Name them `.env.<name>` and you'll access them via `<name>` in `swap-env`.

If you have a local `.env` file (not a symlink), you will be prompted whether to save it first.

```bash
$ ls -A1 ~/.swap-env
.env.dev
.env.test
```

Then simply run `swap-env` and select the file you want to use. A symlink will be created at `./.env` to that file.

```bash
$ swap-env
? Select a .env file:
❯ dev
  test

? Select a .env file: dev

$ ls -l .env
... .env@ -> ~/.swap-env/.env.dev
```

`swap-env` will search upwards from the directory you run it in and use the first `.swap-env/` directory it finds.
If you're not under the home directory, or a `.swap-env/` directory isn't found, `~/.swap-env/` will be used (and created if it doesn't exist).

If you create a `.swap-env/` directory in a git repo, remember to add it to your `.gitignore`.
