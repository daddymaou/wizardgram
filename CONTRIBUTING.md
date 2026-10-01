# Contributing to wizardgram

## Getting Started

1. Fork the repository.
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/wizardgram.git`
3. Install in development mode: `pip install -e ".[dev]"`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Branches and Commits

- Use a short-lived branch for each focused change, such as `fix/retry-after` or `docs/quickstart`.
- Make separate commits for distinct, reviewable changes. Do not split one change into trivial commits just to increase contribution counts.
- Open a pull request from the branch and describe the behavior changed and checks run.
- Keep each commit buildable when practical; combine incidental fixups before opening the pull request.

## Development

- Tests: `pytest`
- Coverage: `pytest --cov`
- Lint: `ruff check .`
- Format: `ruff format .`
- Type check: `mypy src/wizardgram`

Run the full check suite before opening a PR:

    ruff check . && ruff format --check . && mypy src/wizardgram && pytest

## Pull Request Guidelines

- Keep PRs focused on a single change.
- Update docs and examples if you change the public API.
- Add tests for new behavior.
- Follow the Code of Conduct.

## Adding a Bot Template

Bot templates live in examples/. Each template should be:
- A standalone Python file, no package structure.
- Named descriptively: echo_bot.py, menu_bot.py, scene_bot.py.
- Runnable with `WIZARDGRAM_TOKEN=... python examples/echo_bot.py`.
- Documented in examples/README.md with a one-line description.

## Questions

Open a Discussion or an Issue. No question is too basic.