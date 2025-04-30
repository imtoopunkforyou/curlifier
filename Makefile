# === Сonfiguration ===
MAKEFLAGS += --silent
make:
	cat -n ./Makefile

# === Dev ===
lint:
	poetry run flake8 ./curlifier ./tests \
	&& poetry run mypy ./curlifier --no-pretty
pre-commit:
	poetry run isort ./curlifier ./tests \
	&& make lint \
	&& make test
test-collect:
	poetry run pytest ./tests/ --collect-only
test:
	poetry run pytest ./tests/ 

# === Aliases ===
pc: pre-commit
t: test