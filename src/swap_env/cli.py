from pathlib import Path
from InquirerPy import inquirer

from swap_env.dotenv_files import DotenvFiles


def app():
    dotenv_files = DotenvFiles(Path.home().joinpath(".swap_env"))

    dotenv_file_choice = inquirer.select(
        message="Select a .env file", choices=list(dotenv_files), vi_mode=True
    ).execute()

    dotenv_files.link(dotenv_file_choice)
