# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

### Added

- Force edX to use `libcast_xblock` as default video xblock
- Use custom demo course for FUN's flavors

### Fixed

- Add missing setting `LMS_ROOT_URL` used to compute absolute urls
- Fix `GITHUB_REPO_ROOT` and `DATA_DIR` settings

## [eucalyptus.3-wb-1.1.0] - 2019-12-18

### Changed

- Upgrade to nodejs 10 engine

### Fixed

- Rolled back default static files storage backend

## [eucalyptus.3-wb-1.0.5] - 2019-12-16

### Fixed

- Properly configure locales
- Remove duplicated `redis` package installation
- Configure `general` cache backend including cache keys sanitizing function
- Fix broken CMS JS build by enabling Pipeline's static files storage

## [eucalyptus.3-wb-1.0.4] - 2019-12-12

### Changed

- Declare redis as the default session engine

## [eucalyptus.3-wb-1.0.3] - 2019-12-10

### Fixed

- Fix redis release compatibility with celery-redis-sentinel (_e.g._ redis
  2.x.x)

## [eucalyptus.3-wb-1.0.2] - 2019-12-10

### Fixed

- Set CELERY_ACCEPT_CONTENT CMS setting to 'json' to prevent permission issues
  while running in an OpenShift context

## [eucalyptus.3-wb-1.0.1] - 2019-12-04

### Fixed

- Fix SESSION_REDIS_PORT setting definition

## [eucalyptus.3-wb-1.0.0] - 2019-11-14

### Added

- First experimental release of OpenEdx `eucalyptus.3` (wb flavor).
- Set replicaSet and read_preference in mongodb connection
- Add missing support for redis sentinel

[unreleased]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.1.0...HEAD
[eucalyptus.3-wb-1.1.0]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.5...eucalyptus.3-wb-1.1.0
[eucalyptus.3-wb-1.0.5]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.4...eucalyptus.3-wb-1.0.5
[eucalyptus.3-wb-1.0.4]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.3...eucalyptus.3-wb-1.0.4
[eucalyptus.3-wb-1.0.3]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.2...eucalyptus.3-wb-1.0.3
[eucalyptus.3-wb-1.0.2]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.1...eucalyptus.3-wb-1.0.2
[eucalyptus.3-wb-1.0.1]: https://github.com/openfun/openedx-docker/compare/eucalyptus.3-wb-1.0.0...eucalyptus.3-wb-1.0.1
[eucalyptus.3-wb-1.0.0]: https://github.com/openfun/openedx-docker/releases/tag/eucalyptus.3-wb-1.0.0
