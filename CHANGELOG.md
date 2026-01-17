# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-17

### Added

- Add support for Python 3.14.

### Changed

- Migrate from `InquirerPy` to `prompt-toolkit` as `InquirerPy` isn't actively
  maintained. `prompt-toolkit` is now the only direct dependency in the main
  dependency group.
  The process now can't be exited cleanly with `q` or `Esc`. It can only be
  interrupted with `<C-c>`.

### Removed

- Drop support for Python 3.9.

### Documentation

- Recommend installation with uv rather than pipx.
- Add CHANGELOG.

### Chore

- Upgrade uv and dev dependencies.
- Use mise to manage uv and as a task runner.
- Remove GitHub workflows and use mise tasks instead.
- Migrate from GitHub to Codeberg.

## [v1.0.2] - 2024-10-12

### Documentation

- Add README badges.

### Chore

- Migrate from Black to Ruff.
- Upgrade dependencies.
- Migrate from Poetry to uv.
- Add CI workflow.
- Add release workflow triggered by a tag.

## [v1.0.1] - 2024-02-24

### Added

- Add support for Python 3.9 (from requiring >=3.10).

### Testing

- Improve test coverage.
- Change pytest import mode to importlib.

## [v1.0.0] - 2023-04-01

### Added

- Search path upwards for a swap-env directory.

## [v0.2.0] - 2023-03-13

### Added

- Add logic to save existing .env before linking.

## [v0.1.1] - 2023-03-12

Initial functionality using only `~/.swap-env/` and ignoring (?) an existing
`.env` file.
