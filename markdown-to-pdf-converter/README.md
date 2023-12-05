# Feed GPTs

In this repo, we create a single document made of ReScript documention (version 11) and community projects.

## Unify docs and files in one single file

Requirements:

- Python +3.9
- [Poetry](https://pypi.org/project/poetry/): Python dependency management and packaging made easy
- [wkhtmltopdf](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf): Python wrapper to convert HTML to PDF.

Steps to run `main.py`:

1. Change the variables name in `main.py` at the beginning.
2. Run the code

```shell
poetry install
poetry shell
poetry run python3 main.py # Or if you have another Python version, e.g. `poetry run python main.py`
```
