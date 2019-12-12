# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

### Changed

- Declare redis as the default session engine

### Added

- Add Glowbl xblock settings

## [dogwood.3-fun-1.3.4] - 2019-12-10

### Fixed

- Fix redis release compatibility with celery-redis-sentinel (_e.g._ redis
  2.x.x)
- Remove unusable static and media-related paths from settings.yml

## [dogwood.3-fun-1.3.3] - 2019-12-10

### Fixed

- Set CELERY_ACCEPT_CONTENT CMS setting to 'json' to prevent permission issues
  while running in an OpenShift context

## [dogwood.3-fun-1.3.2] - 2019-12-05

### Changed

- Switch ORA2 production backend to Swift
- Make `CELERY_RESULT_BACKEND` configurable

## [dogwood.3-fun-1.3.1] - 2019-12-04

### Fixed

- Fix SESSION_REDIS_PORT setting definition

## [dogwood.3-fun-1.3.0] - 2019-12-02

### Added

- Add missing support for redis sentinel

## [dogwood.3-fun-1.2.1] - 2019-11-29

### Fixed

- Add missing RELEASE setting

## [dogwood.3-fun-1.2.0] - 2019-11-22

### Added

- Set replicaSet and read_preference in mongodb connection

## [dogwood.3-fun-1.1.0] - 2019-11-22

### Added

- FUN production settings carefully splitted between python and yaml files

## [dogwood.3-fun-1.0.0] - 2019-11-07

### Added

- First experimental release of OpenEdx `dogwood.3` (fun flavor).

[unreleased]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.4...HEAD
[dogwood.3-fun-1.3.4]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.3...dogwood.3-fun-1.3.4
[dogwood.3-fun-1.3.3]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.2...dogwood.3-fun-1.3.3
[dogwood.3-fun-1.3.2]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.1...dogwood.3-fun-1.3.2
[dogwood.3-fun-1.3.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.3.0...dogwood.3-fun-1.3.1
[dogwood.3-fun-1.3.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.2.1...dogwood.3-fun-1.3.0
[dogwood.3-fun-1.2.1]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.2.0...dogwood.3-fun-1.2.1
[dogwood.3-fun-1.2.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.1.0...dogwood.3-fun-1.2.0
[dogwood.3-fun-1.1.0]: https://github.com/openfun/openedx-docker/compare/dogwood.3-fun-1.0.0...dogwood.3-fun-1.1.0
[dogwood.3-fun-1.0.0]: https://github.com/openfun/openedx-docker/releases/tag/dogwood.3-fun-1.0.0
