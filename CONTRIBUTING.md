# SECUNIT

# Install For Development
For development use, install using poetry.

```bash
poetry install
``` 
Note, that if installing using poetry, other commands, such as `gunicorn` and `flask` will need to include `poetry run [command]`.
Refer to the [poetry documentation](https://python-poetry.org/) for use of poetry.

# Testing Configuration
To configure the app for testing off target, set the `FLASK_ENV` environment variable to `testing`.
```bash
export FLASK_ENV=testing
```
This will set all GPIO interfaces to mock interfaces, thus allowing testing of the software on other hardware.

## Unit Testing
Run unit testing with pytest.
```bash
poetry run pytest tests
```

## Formatting
Check formatting with flake8.
```bash
poetry run flake8 .
```

Format imports using isort.
```bash
poetry run isort .
```

Format using black.
```bash
poetry run black .
```