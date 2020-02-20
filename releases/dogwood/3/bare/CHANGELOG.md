# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

### Fixed

- Remove hardcoded FILE_UPLOAD_STORAGE_BUCKET_NAME value to make sure it is configurable
- Downgrade and pin `virtualenv` to version 16.7.9

## [dogwood.3-1.2.1] - 2020-01-11

### Removed

- Checks that ensure required directories exist in volumes

## [dogwood.3-1.2.0] - 2020-01-10

### Added

- Make Gunicorn timeout, workers and threads configurable via 
  an environment variable
- Configure all cache backends

### Changed

- Make ORA2 configurable and use filesystem backend by default
- Stop inheriting from MKTG_URL_LINK_MAP default setting

### Fixed

- Ensure all required directories exist inside each volume
- Refactor settings to repair and clean what is cms versus lms, configurable
  versus defined by code.

## [dogwood.3-1.1.5] - 2019-12-24

### Fixed

- `AUTH_TOKENS` was wrongly used as a dictionary and default values were lost

## [dogwood.3-1.1.4] - 2019-12-19

### Fixed

- Add missing setting `LMS_ROOT_URL` used to compute absolute urls
- Fix broken CMS JS build by enabling Pipeline's static files storage
- Configure `general` cache backend including cache keys sanitizing function
- Fix `GITHUB_REPO_ROOT` and `DATA_DIR` settings

## [dogwood.3-1.1.3] - 2019-12-15

### Fixed

- Properly configure locales
- Use pyOpenSSL instead of local openssl library for SSL certificate checking

## [dogwood.3-1.1.2] - 2019-12-10

### Fixed

- Set CELERY_ACCEPT_CONTENT CMS setting to 'json' to prevent permission issues
  while running in an OpenShift context

## [dogwood.3-1.1.1] - 2019-11-29

### Fixed

- Add missing RELEASE setting

## [dogwood.3-1.1.0] - 2019-10-10

### Changed

- Add LOCALE_PATHS to configurable settings

## [dogwood.3-1.0.0] - 2019-09-24

### Added

First experimental release of OpenEdx `dogwood.3` (bare flavor).

[unreleased]: https://github.com/openfun/openedx-docker/compare/dogwood.3-1.2.1...HEAD
[dogwood.3-1.2.1]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.2.0...dogwood.3-1.2.1
[dogwood.3-1.2.0]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.1.5...dogwood.3-1.2.0
[dogwood.3-1.1.5]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.1.4...dogwood.3-1.1.5
[dogwood.3-1.1.4]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.1.3...dogwood.3-1.1.4
[dogwood.3-1.1.3]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.1.2...dogwood.3-1.1.3
[dogwood.3-1.1.2]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.1.1...dogwood.3-1.1.2
[dogwood.3-1.1.1]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.1.0...dogwood.3-1.1.1
[dogwood.3-1.1.0]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.0.0...dogwood.3-1.1.0
[dogwood.3-1.0.0]: https://github.com/openfun/openedx-docker/releases/tag/dogwood.3-1.0.0
