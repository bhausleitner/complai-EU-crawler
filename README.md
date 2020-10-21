# COMPLAI Regulatory Data Collection

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Setup

1. Activate the Python version you want to use with [pyenv](https://github.com/pyenv/pyenv)

To create a clean Python environment use pyenv, which is a tool to manage different Python versions. If you do not have it on your system already, follow [this](https://realpython.com/intro-to-pyenv/) great guide by Real Python. Then simply run the following commands:

```bash
pyenv install 3.7.7
pyenv global 3.7.7
```

2. Install dependencies with [Poetry](https://python-poetry.org)
Install Poetry by following the install instructions for your OS on their [website](https://python-poetry.org/docs/#installation). Then run the following commands to install the dependecies:

```bash
poetry install
```

3. Install [pre-commit](https://pre-commit.com) hooks from `.pre-commit-config.yaml`

```bash
poetry run pre-commit install
```

4. Run the tests

```bash
poetry run pytest
```

## Run eur_lex_webservice

```bash
poetry run eur_lex_webservice
```
