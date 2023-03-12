from pathlib import Path
from InquirerPy import inquirer

from swap_env.dotenv_files import DotenvFiles


keybindings = {
    "answer": [{"key": "enter"}],  # answer the prompt
    "interrupt": [{"key": "c-c"}],  # raise KeyboardInterrupt
    "skip": [{"key": "q"}, {"key": "escape"}],  # skip the prompt
}


def app():
    dotenv_files = DotenvFiles(Path.home().joinpath(".swap-env"))

    dotenv_file_choice = inquirer.select(
        message="Select a .env file",
        choices=list(dotenv_files),
        vi_mode=True,
        mandatory=False,
        keybindings=keybindings,
    ).execute()

    if dotenv_file_choice is None:
        return

    dotenv_files.link(dotenv_file_choice)
