# === Сonfiguration ===
MAKEFLAGS += --silent
make:
	cat -n ./Makefile

# === Dev ===
lint:
	poetry run flake8 ./curlifier ./tests \
	&& poetry run mypy ./curlifier --no-pretty \
	&& make test
pre-commit:
	poetry run isort ./curlifier ./tests && make lint
nitpick:
	poetry run nitpick fix
test:
	poetry run pytest ./tests

# === Aliases ===
pc: pre-commit
np: nitpick
t: test