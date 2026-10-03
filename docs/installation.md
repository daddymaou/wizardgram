# Installation

wizardgram requires Python 3.10 or newer and is available on PyPI.

## Install from PyPI

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install wizardgram
```

### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install wizardgram
```

## Development install

For local development, install the project in editable mode with its dev tools:

```bash
python -m pip install -e ".[dev]"
```

To build the documentation locally, install the docs extra and run MkDocs:

```bash
python -m pip install -e ".[docs]"
mkdocs serve
```

The Telegram bot token is not part of installation. Keep it in an environment
variable such as `WIZARDGRAM_TOKEN`; see the [quickstart](quickstart.md).