# Changelog

All notable changes to SudaPy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-01

### Changed

- **Breaking:** GDAL-dependent packages (`geopandas`, `shapely`, `fiona`, `rasterio`, `numpy`) moved from core dependencies to the new `[geo]` optional extra. `pip install sudapy` now works on any platform without GDAL.
- `reproject_raster()` `resampling` parameter now accepts a string (`"nearest"`, `"bilinear"`, `"cubic"`) instead of a `rasterio.warp.Resampling` enum value.
- `sudapy doctor` now labels geo dependencies as optional and shows `SKIP` (yellow) instead of `FAIL` when they are missing.

### Added

- `require_extra()` helper in `sudapy.core.errors` for lazy-importing optional dependencies with clear install hints.
- New `[geo]` install extra: `pip install "sudapy[geo]"` for vector/raster operations.
- `[viz]` extra now automatically includes `[geo]`.
- `[all]` extra now includes `[geo]`, `[viz]`, and `[rs]`.
- Clear `DependencyError` messages when calling vector/raster/viz functions without `[geo]` installed.

### Fixed

- `pip install sudapy` no longer fails on Windows due to missing GDAL C libraries.

## [1.0.2] - 2026-02-01

### Fixed

- Documentation URL on PyPI now points to GitHub Pages docs site.

### Added

- Comprehensive MkDocs Material documentation (20 pages).

## [1.0.1] - 2026-02-01

### Fixed

- Project URLs now point to correct GitHub repository (Osman-Geomatics93/sudapy).
- INSTALL_OFFLINE.md link uses absolute GitHub URL (no longer 404s on PyPI).
- Version/classifier alignment: 1.x with Production/Stable status.

## [1.0.0] - 2026-02-01

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
