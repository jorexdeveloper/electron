<h1 align="center">ELECTRON</h1>

<div align="center" style="color: red; font-weight: bold;">
    This project is in early development. Features and functionality are subject to change.
    Contributors are welcome!
</div>

<p align="center">
    <a href="https://github.com/jorexdeveloper/electron/stargazers">
        <img src="https://img.shields.io/github/stars/jorexdeveloper/electron?colorA=23272a&colorB=007bff&style=for-the-badge">
    </a>
    <a href="https://github.com/jorexdeveloper/electron/issues">
        <img src="https://img.shields.io/github/issues/jorexdeveloper/electron?colorA=23272a&colorB=ff4500&style=for-the-badge">
    </a>
    <a href="https://github.com/jorexdeveloper/electron/contributors">
        <img src="https://img.shields.io/github/contributors/jorexdeveloper/electron?colorA=23272a&colorB=28a745&style=for-the-badge">
    </a>
</p>

<div align="center" style="background-color:black;border:3px solid black;border-radius:6px;margin:5px 0;padding:2px 5px">
    <img src="./logo.jpeg" alt="logo" style="color:red;background-color:black;font-weight:bold" />
</div>

**Electron** is powerful, easy to use command-line AI assistant inspired by J.A.R.V.I.S.

## Why use Electron?

Whether you're a developer, researcher, or just someone who is looking to experiment with AI in your terminal, Electron is for you! It offers:

-   Seamless natural language interaction in the terminal.
-   Integration with different AI models for enhanced productivity.
-   Customizable workflows tailored to your needs.

Basically, forget typing complex shell commands in your terminal and simply instruct Electron to do it for you using natural language.

<details>
    <summary>Contents</summary>
    <ul class="simple" title="View this section.">
        <li><a href="#features" title="View this section.">Features</a></li>
        <li><a href="#getting-started" title="View this section.">Getting Started</a></li>
        <ul>
            <li><a href="#installation" title="View this section.">Installation</a></li>
            <li><a href="#configuration" title="View this section.">Configuration</a></li>
        </ul>
        <li><a href="#usage" title="View this section.">Usage</a></li>
        <ul>
            <li><a href="#basic-commands" title="View this section.">Basic Commands</a></li>
            <li><a href="#advanced-usage" title="View this section.">Advanced Usage</a></li>
        </ul>
        <li><a href="#troubleshooting" title="View this section.">Troubleshooting</a></li>
        <li><a href="#faq" title="View this section.">FAQ</a></li>
        <li><a href="#contribution" title="View this section.">Contribution</a></li>
        <li><a href="#license" title="View this section.">License</a></li>
    </ul>
</details>

## Features

-   **Natural Language Understanding**: Communicate with Electron using natural language.
-   **Inbuilt Terminal Support**: Send commands to your terminal using Electron.
-   **API Integration**: Connect with various APIs and tools for enhanced functionality.
-   **Customizable Workflows**: Tailor commands and workflows to suit your needs.
-   **Interaction History**: View and manage past interactions with the assistant.
-   **Markdown Support**: Displays responses in rich Markdown format for better readability.

## Getting Started

Get a free/paid AI/ML API key from [here](/link_here "AI/ML website") and save it somewhere, you will need it for authenticatication while using the assistant.

### Installation

Now open your terminal and:

1. Clone the repository:
    ```bash
    git clone https://github.com/jorexdeveloper/electron.git
    ```
    Or download and extract files from the [latest release](/link_here "The latest release of Electron.").
2. Navigate to the project directory and execute the installer:
    ```bash
    bash electron/install.sh
    ```
    This will interactively install everything in the repository directory, so that you can rename and move it anywhere without any conflicts.

### Configuration

Electron requires a configuration file (`settings.json`) to function properly, but don't worry, a new ome with default values will be created if it's missing You can customize the following keys:

-   **`model`**: The AI model to use (default: `gpt-4o-mini`).
-   **`api_key`**: Your API key for authentication. If left empty, its got from the environment as `API_KEY`
-   **`system_message`**: The assistant's context message.
-   **`assistant_name`**: The name of the assistant (default: `Electron`).
-   **`user_name`**: Your name for personalized interactions.

## 💻 Usage

### Basic Commands

Run the Electron assistant using the following command:

```bash
python electron.py
```

Once running, you can interact with Electron using natural language commands. For example:

```bash
> What is the weather today?
> Create a new file named "example.txt".
```

### Advanced Usage

-   **View Interaction History**:
    ```bash
    history
    history 5
    ```
-   **Exit Commands**:
    Use any of the following commands to exit:
    ```bash
    q, quit, exit, bye, close, stop
    ```

## 🛠️ Troubleshooting

### Common Issues

-   **Missing API Key**:
    If you see an error about a missing API key, ensure you have set it in the `settings.json` file or as an environment variable.

-   **Connection Errors**:
    Check your internet connection and ensure the API endpoint is reachable.

## ❓ FAQ

### What happens if I don't set an API key?

Electron requires an API key to function. If the key is missing, you will be prompted to provide one during the first run.

### Can I customize the assistant's name?

Yes! You can change the assistant's name by editing the `assistant_name` field in the `settings.json` file.

## 🤝 Contribution

Contributions to this project are not only welcome but also encouraged.

Here is the current TODO list:

1. Add more commands and workflows for common tasks.
2. Improve error handling and logging.
3. Enhance the configuration process for better user experience.

Feel free to fork the repository, make your changes, and submit a pull request. Let's make Electron even better together!

## 📜 License

```txt
    Copyright (C) 2025  Jore

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
