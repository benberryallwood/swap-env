from pathlib import Path

from prompt_toolkit.shortcuts import choice, confirm, prompt
from prompt_toolkit.validation import Validator

from swap_env.dotenv_dir import search_fs_for_dotenv_dir
from swap_env.dotenv_files import DotenvFiles


def prompt_to_save_current_file_if_exists(dotenv_files: DotenvFiles) -> None:
    local_dotenv_path = Path.cwd().joinpath(".env")
    if not local_dotenv_path.exists() or local_dotenv_path.is_symlink():
        return

    save_local_file = confirm(
        "A .env file already exists, do you want to save this before continuing?"
    )

    if not save_local_file:
        return

    new_dotenv_name = prompt(
        "Enter a name for this .env file: ",
        validator=Validator.from_callable(
            lambda name: name not in dotenv_files and name != "",
            error_message="The name is empty or already exists",
        ),
    )

    dotenv_files.save_local_dotenv(name=new_dotenv_name)


def app():
    dotenv_dir = search_fs_for_dotenv_dir()
    dotenv_files = DotenvFiles(path=dotenv_dir)

    prompt_to_save_current_file_if_exists(dotenv_files=dotenv_files)

    if not dotenv_files:
        print(f"No dotenv files found in {dotenv_files.path}")
        return

    dotenv_file_choice = choice(
        "Select a .env file:",
        options=[(name, name) for name in dotenv_files],
    )

    dotenv_files.link(dotenv_file_choice)
