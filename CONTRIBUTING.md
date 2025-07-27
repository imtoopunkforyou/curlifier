# How to contribute

## Steps

- Make sure you have a [GitHub account](https://github.com/signup/free).
- Submit a ticket for your issue, assuming one does not already exist.
- Fork the repository on GitHub.
- Apply the required changes!
- Briefly describe the changes you have made. We do this in [CHANGELOG.md](https://github.com/imtoopunkforyou/curlifier/blob/main/CHANGELOG.md).
- Send a Pull Request to our original repo. Here's the [helpful guide](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) on how to do that.

## Making Changes

- We use [poetry](https://python-poetry.org/docs/#installation) to manage the project and you should have it installed. To install a local version of `Python 3.10.*`, we recommend using [pyenv](https://github.com/pyenv/pyenv).
- Follow our coding style. You can run `make lint` to check your code.
- To run the tests, type `make test`.
- To check your code style and run tests at the same time, type `make pre-commit`.
- No matter how many commits your PR has, the commits will be squashed before merging.
