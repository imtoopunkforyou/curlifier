# === Сonfiguration ===
MAKEFLAGS += --silent
make:
	cat -n ./Makefile

# === Dev ===
lint:
	poetry run ruff check ./curlifier ./tests \
	&& poetry run ruff format ./curlifier ./tests \
    && poetry run flake8 ./curlifier ./tests \
	&& poetry run mypy ./curlifier --no-pretty
pre-commit:
	make lint \
	&& make test
test-collect:
	poetry run pytest ./tests/ --collect-only
test:
	poetry run pytest ./tests/ 

# === Aliases ===
pc: pre-commit
t: test