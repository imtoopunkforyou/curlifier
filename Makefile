# === Сonfiguration ===
MAKEFLAGS += --silent
make:
	cat -n ./Makefile

# === Dev ===
lint:
	poetry run ruff check ./curlifier ./tests \
	&& poetry run ruff format ./curlifier ./tests \
	&& poetry run flake8 ./curlifier \
	&& poetry run mypy ./curlifier --no-pretty
pre-commit:
	make lint \
	&& make test
test-collect:
	poetry run pytest ./tests/ --collect-only
test:
	poetry run pytest ./tests/ 
cov-report:
	poetry run pytest ./tests --cov=curlifier --cov-report=html

# === Aliases ===
pc: pre-commit
t: test