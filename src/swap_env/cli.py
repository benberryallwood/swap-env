from pathlib import Path
from typing import Optional
from InquirerPy import inquirer

from swap_env.dotenv_files import DotenvFiles


DOTENV_DIR = Path.home().joinpath(".swap-env")

keybindings = {
    "answer": [{"key": "enter"}],  # answer the prompt
    "interrupt": [{"key": "c-c"}],  # raise KeyboardInterrupt
    "skip": [{"key": "q"}, {"key": "escape"}],  # skip the prompt
}


def app():
    dotenv_files = DotenvFiles(path=DOTENV_DIR)

    if not dotenv_files:
        print("There are no .env files in ~/.swap-env/")
        return

    dotenv_file_choice: Optional[str] = inquirer.select(
        message="Select a .env file",
        choices=list(dotenv_files),
        vi_mode=True,
        mandatory=False,
        keybindings=keybindings,
    ).execute()

    if dotenv_file_choice is None:  # prompt skipped with 'q' or 'escape'
        return

    dotenv_files.link(dotenv_file_choice)
