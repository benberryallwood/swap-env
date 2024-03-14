from __future__ import annotations

from pathlib import Path

from InquirerPy import inquirer

from swap_env.dotenv_dir import search_fs_for_dotenv_dir
from swap_env.dotenv_files import DotenvFiles

keybindings = {
    "answer": [{"key": "enter"}],  # answer the prompt
    "interrupt": [{"key": "c-c"}],  # raise KeyboardInterrupt
    "skip": [{"key": "q"}, {"key": "escape"}],  # skip the prompt
}


def prompt_to_save_current_file_if_exists(dotenv_files: DotenvFiles) -> None:
    local_dotenv_path = Path.cwd().joinpath(".env")
    if not local_dotenv_path.exists() or local_dotenv_path.is_symlink():
        return

    save_local_file = inquirer.confirm(
        message="A .env file already exists, do you want to save this before continuing?",
        default=True,
    ).execute()

    if not save_local_file:
        return

    new_dotenv_name = inquirer.text(
        message="Enter a name for this .env file:",
        validate=lambda name: name not in dotenv_files and name != "",
        invalid_message="The name is empty or already exists",
    ).execute()

    dotenv_files.save_local_dotenv(name=new_dotenv_name)


def app():
    dotenv_dir = search_fs_for_dotenv_dir()
    dotenv_files = DotenvFiles(path=dotenv_dir)

    prompt_to_save_current_file_if_exists(dotenv_files=dotenv_files)

    if not dotenv_files:
        print(f"No dotenv files found in {dotenv_files.path}")
        return

    dotenv_file_choice: str | None = inquirer.select(
        message="Select a .env file:",
        choices=list(dotenv_files),
        vi_mode=True,
        mandatory=False,
        keybindings=keybindings,
    ).execute()

    if dotenv_file_choice is None:  # prompt skipped with 'q' or 'escape'
        return

    dotenv_files.link(dotenv_file_choice)
