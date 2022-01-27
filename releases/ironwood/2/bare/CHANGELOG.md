# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) for each flavored OpenEdx
release.

## [Unreleased]

### Changed

- Use Nginx Inc's unprivileged image instead of our custom image for OpenShift

## [ironwood.2-1.0.1] - 2021-09-28

### Fixed

- Set `SESSION_COOKIE_SECURE` to True by default
- Fix build by installing py2neo 3.1.2 from its github repository
- Fix pip install for python 2.7

## [ironwood.2-1.0.0] - 2020-09-10

- First release of an `ironwood.2-bare` Docker image.

[unreleased]: https://github.com/openfun/openedx-docker/compare/ironwood.2-1.0.1...HEAD
[ironwood.2-1.0.1]: https://github.com/openfun/openedx-docker/compare/ironwood.2-1.0.0...ironwood.2-1.0.1
