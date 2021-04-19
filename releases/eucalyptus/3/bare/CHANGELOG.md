# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

### Fixed

- Fix build after get-pip.py script moved location

## [eucalyptus.3-1.2.0] - 2020-05-14

### Added

- Allow serving static files via a CDN
- Rate limiting authentication backend that works behind proxies

### Changed

- Collect static files in the `edxapp` image so it can run without mounting a volume
  for its static files in Kubernetes
- Refactor the way authentication backends are configured to make it straightforward
- Set basic authentification backend for development environment

## [eucalyptus.3-1.1.2] - 2020-03-13

### Fixed

- Fix setting `AUTHENTICATION_BACKENDS` to allow activating third party authentication
- Remove hardcoded FILE_UPLOAD_STORAGE_BUCKET_NAME value to make sure it is configurable

## [eucalyptus.3-1.1.1] - 2020-01-11

### Removed

- Checks that ensure required directories exist in volumes

## [eucalyptus.3-1.1.0] - 2020-01-10

### Added

- Make Gunicorn timeout, workers and threads configurable via an environment
  variable
- Configure all cache backends

### Changed

- Make ORA2 configurable and use filesystem backend by default
- Stop inheriting from MKTG_URL_LINK_MAP default setting

### Removed

- Alternate queues settings to extend CELERY_QUEUES for cross-process workers

### Fixed

- Ensure all required directories exist inside each volume
- Refactor settings to repair and clean what is cms versus lms, configurable
  versus defined by code.

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

[unreleased]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.2.0...HEAD
[eucalyptus.3-1.2.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.1.2...eucalyptus.3-1.2.0
[eucalyptus.3-1.1.2]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.1.1...eucalyptus.3-1.1.2
[eucalyptus.3-1.1.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.1.0...eucalyptus.3-1.1.1
[eucalyptus.3-1.1.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.4...eucalyptus.3-1.1.0
[eucalyptus.3-1.0.4]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.3...eucalyptus.3-1.0.4
[eucalyptus.3-1.0.3]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.2...eucalyptus.3-1.0.3
[eucalyptus.3-1.0.2]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.1...eucalyptus.3-1.0.2
[eucalyptus.3-1.0.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-1.0.0...eucalyptus.3-1.0.1
[eucalyptus.3-1.0.0]: https://github.com/openfun/openedx-docker/releases/tag/eucalyptus.3-1.0.0
