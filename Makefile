# === Configuration ===
MAKEFLAGS += --silent
make:
	cat -n ./Makefile

# === Dev ===
.PHONY: lint
lint:
	poetry run ruff check ./curlifier ./tests \
	&& poetry run ruff format ./curlifier ./tests \
	&& poetry run flake8 ./curlifier \
	&& poetry run mypy ./curlifier --no-pretty

.PHONY: pre-commit
pre-commit:
	make lint \
	&& make test \
	&& make spell-check

.PHONY: spell-check
spell-check:
	poetry run codespell curlifier tests README.md CONTRIBUTING.md

.PHONY: test-collect
test-collect:
	poetry run pytest ./tests/ --collect-only

.PHONY: test
test:
	poetry run pytest ./tests/

.PHONY: cov-report
cov-report:
	poetry run pytest ./tests --cov=curlifier --cov-report=html

.PHONY: cspell
cspell:
	npx cspell-cli --gitignore .

# === Aliases ===
pc: pre-commit
t: test
