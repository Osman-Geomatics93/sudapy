# Changelog

All notable changes to SudaPy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-02-01

### Added

- Initial release of SudaPy.
- Built-in CRS presets for Sudan: WGS 84 UTM zones 34-37N, Adindan UTM zones 35-37N.
- CRS suggestion engine (`sudapy crs suggest`) for automatic UTM zone detection.
- Vector operations: reproject, clip, dissolve, area calculation, buffer, simplify, fix-geometry.
- Raster operations: clip by vector, reproject, resample, mosaic, hillshade, slope.
- Quick map visualization export to PNG and interactive HTML.
- `sudapy doctor` command for environment diagnostics.
- `sudapy init` command for project scaffolding.
- `sudapy report` command for dataset summary.
- `sudapy batch` command for batch processing.
- Remote sensing Sentinel search/download (optional `[rs]` extra).
- Offline installation support with wheelhouse builder script.
- conda `environment.yml` for known-good geospatial setup.
- GitHub Actions CI for Linux and Windows.
- Full test suite for CRS logic, vector operations, and area calculations.
