# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

### Added

- Make Gunicorn timeout configurable via an environment variable

## [eucalyptus.3-1.0.4] - 2019-12-24

### Fixed

- `AUTH_TOKENS` was wrongly used as a dictionary and default values were lost

## [eucalyptus.3-1.0.3] - 2019-12-19

### Fixed

- Upgrade to nodejs 10 engine to repair failing image build
- Add missing setting `LMS_ROOT_URL` used to compute absolute urls
- Configure `general` cache backend including cache keys sanitizing function
- Properly configure locales
- Fix `GITHUB_REPO_ROOT` and `DATA_DIR` settings

## [eucalyptus.3-1.0.2] - 2019-12-10

### Fixed

- Set CELERY_ACCEPT_CONTENT CMS setting to 'json' to prevent permission issues
  while running in an OpenShift context

## [eucalyptus.3-1.0.1] - 2019-11-29

### Fixed

- Add missing RELEASE setting

## [eucalyptus.3-1.0.0] - 2019-11-06

### Added

- First experimental release of OpenEdx `eucalyptus.3` (bare flavor).

[unreleased]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.4...HEAD
[eucalyptus.3-1.0.4]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.3...eucalyptus.3-1.0.4
[eucalyptus.3-1.0.3]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.2...eucalyptus.3-1.0.3
[eucalyptus.3-1.0.2]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.1...eucalyptus.3-1.0.2
[eucalyptus.3-1.0.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.0...eucalyptus.3-1.0.1
[eucalyptus.3-1.0.0]: https://github.com/openfun/openedx-docker/releases/tag/eucalyptus.3-1.0.0
