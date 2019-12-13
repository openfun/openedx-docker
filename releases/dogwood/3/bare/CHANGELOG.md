# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

### Fixed

- Properly configure locales

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

[unreleased]: https://github.com/openfun/openedx-docker/compare/dogwood.3-1.1.2...HEAD
[dogwood.3-1.1.2]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.1.1...dogwood.3-1.1.2
[dogwood.3-1.1.1]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.1.0...dogwood.3-1.1.1
[dogwood.3-1.1.0]: https://github.com/openfun/openedx-docker/compare/tag/dogwood.3-1.0.0...dogwood.3-1.1.0
[dogwood.3-1.0.0]: https://github.com/openfun/openedx-docker/releases/tag/dogwood.3-1.0.0
