import os
import sys
import json
import logging

from typing import Dict
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

API_KEY_NAME = "API_KEY"
BASE_URL = "https://api.aimlapi.com/v1"
INTERACTION_HISTORY_LIMIT = 10
SETTINGS_FILE = "settings.json"
HISTORY_FILE = "history.json"
REQUIRED_KEYS = [
    "model", "api_key", "system_message", "assistant_name", "user_name"]
DEFAULT_SETTINGS = {
    "model": "gpt-4o-mini",
    "api_key": "",
    "system_message": "You are {assistant_name}, a command line AI assistant for {user_name} who knows everything.",
    "assistant_name": "Electron",
    "user_name": "User"
}
EXIT_COMMANDS = [
    "q", "quit", "exit", "bye", "close", "stop", "end", "terminate", "leave"]
CONFIRMATION_COMMANDS = [
    "yes", "y", "yeah", "yep", "sure", "ok", "okay", "fine"]
HELP_MESSAGE = f"""\
I am here to assist you with anything. \
"""
CONSOLE = Console()
logging.basicConfig(filename="electron.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def msg(content: str, markdown: bool = False, bold: bool = False,
        color: str = None, begin: str = "\n", end: str = "\n") -> None:
    """
    Print a message to the console with optional formatting.
    Args:
        content (str): The message content.
        markdown (bool): Render as Markdown if True.
        bold (bool): Render in bold if True.
        color (str): Optional color for the message.
        begin (str): String prepended before the message.
        end (str): String appended after the message.
    Returns:
        None
    """
    if bold:
        content = f"[bold]{content}[/bold]"
    if color:
        content = f"[{color}]{content}[/{color}]"
    CONSOLE.print(begin, end="")
    CONSOLE.print(Markdown(content) if markdown else content, end="")
    CONSOLE.print(end, end="")


def load_settings(config_file_path: str) -> Dict[str, str]:
    """
    Load settings from a JSON file or create defaults if missing.
    Args:
        config_file_path (str): Path to the settings file.
    Returns:
        Dict[str, str]: Parsed settings data.
    Raises:
        ValueError: If required keys are missing.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with open(config_file_path, "r") as file:
            config = json.load(file)
        for key in REQUIRED_KEYS:
            if key not in config:
                raise ValueError(f"Missing required key: '{key}' in settings.")
        return config
    except FileNotFoundError:
        logging.warning(
            f"Settings file not found at '{config_file_path}'. Using default settings.")
        write_default_config(config_file_path)
        return DEFAULT_SETTINGS.copy()
    except json.JSONDecodeError:
        logging.error(
            f"Invalid JSON in settings file: '{config_file_path}'. Using default settings.")
        write_default_config(config_file_path)
        return DEFAULT_SETTINGS.copy()


def load_history(history_file_path: str, limit: int = None) -> list:
    """
    Load interaction history from a file.
    Args:
        history_file_path (str): Path to the history file.
        limit (int): Number of interactions to load. Load all if None.
    Returns:
        list: List of interaction history as dictionaries.
    """
    if not os.path.exists(history_file_path) or os.path.getsize(
            history_file_path) == 0:
        return []

    def read_lines(file_path: str) -> iter:
        """Generator to read lines from a file.
        Args:
            file_path (str): Path to the file to read.
        Yields:
            str: A line from the file, stripped of leading/trailing whitespace.
        """
        with open(file_path, "r") as file:
            for line in file:
                yield line.strip()
    try:
        history = [json.loads(line)
                   for line in (list(read_lines(history_file_path))[-limit:] if limit else read_lines(history_file_path)) if line]
        return history
    except json.JSONDecodeError:
        logging.error(
            f"Failed to load history: The file '{history_file_path}' may be corrupted.")
        return []


def write_default_config(config_file_path: str) -> None:
    """
    Write default settings to a file if it doesn't exist or is empty.
    Args:
        config_file_path (str): Path to the settings file.
    Returns:
        None
    """
    if not os.path.exists(config_file_path) or os.path.getsize(
            config_file_path) == 0:
        try:
            logging.warning(
                f"Writing default settings to '{config_file_path}'.")
            with open(config_file_path, "w") as file:
                json.dump(DEFAULT_SETTINGS, file, indent=4)
            logging.info(f"Default settings written to '{config_file_path}'.")
        except Exception as error:
            logging.error(
                f"Failed to write the default settings to '{config_file_path}': {error}")
    else:
        logging.warning(
            f"Default settings not written: Settings file ('{config_file_path}') already exists and is not empty.")


def initialize_client(api_key: str) -> OpenAI:
    """
    Initialize the OpenAI client.
    Args:
        api_key (str): API key for authentication.
    Returns:
        OpenAI: Initialized OpenAI client.
    """
    return OpenAI(api_key=api_key, base_url=BASE_URL)


def generate_response(client: OpenAI, model: str,
                      system_message: str, interaction_history: list) -> str:
    """
    Generate a response using the assistant model.
    Args:
        client (OpenAI): Initialized OpenAI client.
        model (str): Model to use for generating responses.
        system_message (str): Context message for the assistant.
        interaction_history (list): List of recent interactions.
    Returns:
        str: Assistant's response message.
    """
    messages = [{"role": "system", "content": system_message}] + \
        interaction_history
    response = client.chat.completions.create(model=model, messages=messages,)
    return response.choices[0].message.content


def print_response(assistant_name: str, assistant_message: str) -> None:
    """
    Print the assistant's response in Markdown format.
    Args:
        assistant_name (str): Name of the assistant.
        assistant_message (str): Message generated by the assistant.
    Returns:
        None
    """
    msg(f"**{assistant_name}**: {assistant_message}", markdown=True)


def exit_assistant(status: int = 0,
                   message: str = "Goodbye! See you later.") -> None:
    """
    Exit the assistant with a message.
    Args:
        status (int): Exit status code.
        message (str): Message to display before exiting.
    Returns:
        None
    """
    msg(message, bold=True, color="green" if status == 0 else "red")
    sys.exit(status)


def print_history(user_name: str, assistant_name: str,
                  history_file_path: str, n: int = None) -> None:
    """
    Display interaction history.
    Args:
        user_name (str): Name of the user.
        assistant_name (str): Name of the assistant.
        history_file_path (str): Path to the history file.
        n (int, optional): Number of entries to display. Defaults to None.
    Returns:
        None
    """
    history = load_history(history_file_path)
    if not history:
        msg("No conversations found. Start a discussion to create history!",
            bold=True, color="yellow", end="\n\n")
        return
    if n is not None:
        history = history[-n:]
    if n == 1:
        msg("## Last message", markdown=True)
    elif n == 0 or n is None:
        msg("## Full conversation history", markdown=True)
    else:
        msg(f"## Last {n} messages", markdown=True)
    msg("***", markdown=True)
    for entry in history:
        role = entry.get("role", "unknown")
        content = entry.get("content", "")
        msg(f"**{user_name if role == 'user' else assistant_name}**: {content}", markdown=True)
    msg("***", markdown=True)


def print_help_msg(assistant_name: str, commands=None) -> None:
    """
    Print a help message for the assistant.
    Args:
        assistant_name (str): Name of the assistant.
        commands (optional): List or dictionary of commands for specific help.
    Returns:
        None
    """
    # TODO: Create help method that can provide help on any
    # command given
    print_response(assistant_name, HELP_MESSAGE)


def request_for_api_key() -> str:
    """
    Prompt the user to provide an API key and optionally save it for future use.
    Returns:
        str: The API key entered by the user.
    Exits:
        Exits with status code 1 if the user declines to provide the API key.
    """
    msg(f"Your API key is missing in '{SETTINGS_FILE}' and is not set in the environment as '{API_KEY_NAME}'!\nWould you like to set it now?",
        bold=True, color="yellow", end=": ")
    response = input().strip().lower()
    if response in CONFIRMATION_COMMANDS:
        api_key = ""
        msg("Input your API key", bold=True, color="yellow", end=": ")
        while not api_key:
            api_key = input().strip()
        msg("Save API key for future use?", bold=True, color="yellow", end=": ")
        save_response = input().strip().lower()
        if save_response in CONFIRMATION_COMMANDS:
            try:
                with open(SETTINGS_FILE, "r+") as file:
                    config = json.load(file)
                    config["api_key"] = api_key
                    file.seek(0)
                    json.dump(config, file, indent=4)
                    file.truncate()
                msg("API key saved.", bold=True, color="green")
            except Exception as error:
                logging.error(f"Failed to save API key: {error}")
                msg("API key not saved. See logs for more info.",
                    bold=True, color="red")
        else:
            msg("API key not saved.", bold=True, color="yellow")
        return api_key
    else:
        exit_assistant(1, "Set your API key and try again.")


def write_to_history(file, interaction: dict) -> None:
    """
    Write a single interaction to the history file and flush the changes.
    Args:
        file: The file object for the history file.
        interaction (dict): The interaction to write.
    Returns:
        None
    """
    file.write(json.dumps(interaction) + "\n")
    file.flush()


def main() -> None:
    """
    Run the AI assistant.
    Returns:
        None
    """
    try:
        config = load_settings(
            os.path.join(os.path.dirname(__file__), SETTINGS_FILE))
        model = config["model"]
        api_key = config["api_key"]
        user_name = config["user_name"]
        assistant_name = config["assistant_name"]
        system_message = config["system_message"].format(
            assistant_name=assistant_name, user_name=user_name)
        if not config["api_key"]:
            config["api_key"] = os.environ.get(
                API_KEY_NAME) or request_for_api_key()
        client = initialize_client(api_key)
        user_message = " ".join(sys.argv[1:])
        history_file_path = os.path.join(
            os.path.dirname(__file__), HISTORY_FILE)
        interaction_history = load_history(
            history_file_path, INTERACTION_HISTORY_LIMIT)
        with open(history_file_path, "a") as history_file:
            while True:
                msg(f"{user_name}", bold=True, end=": ")
                if not user_message:
                    while not user_message:
                        user_message = input().strip()
                else:
                    msg(user_message, begin="")
                msg("", end="")
                match user_message.lower().split():
                    case command if command[0] in EXIT_COMMANDS:
                        exit_assistant()
                    case ["help", *args]:
                        print_help_msg(assistant_name)
                        user_message = ""
                        continue
                    case ["history", *args]:
                        try:
                            n = int(args[0]) if args else None
                            print_history(
                                user_name, assistant_name, history_file_path, n)
                        except ValueError:
                            msg("Invalid argument for history. Please provide a number.",
                                bold=True, color="yellow")
                        user_message = ""
                        continue
                user_interaction = {"role": "user", "content": user_message}
                interaction_history.append(user_interaction)
                write_to_history(history_file, user_interaction)
                try:
                    assistant_message = generate_response(
                        client, model, system_message, interaction_history)
                    print_response(assistant_name, assistant_message)
                    ai_interaction = {
                        "role": "assistant", "content": assistant_message}
                    interaction_history.append(ai_interaction)
                    write_to_history(history_file, ai_interaction)
                    interaction_history = interaction_history[-INTERACTION_HISTORY_LIMIT:]
                except Exception as error:
                    logging.error(
                        f"Error generating response: {error}, see logs for more info.")
                    msg(f"Error generating response: {error}",
                        bold=True, color="red", end="\n\n")
                    write_to_history(
                        history_file, {"role": "assistant", "content": "null"})
                user_message = ""
    except (EOFError, KeyboardInterrupt):
        logging.info("Session ended by user.")
        exit_assistant(message="Session ended. Goodbye!")
    except Exception as error:
        logging.critical(f"Unexpected error: {error}")
        exit_assistant(
            1, f"Unexpected error: {error}, see logs for more info.")


if __name__ == "__main__":
    main()
