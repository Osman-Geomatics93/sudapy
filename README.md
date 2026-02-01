# SudaPy

**Sudan-focused Python toolkit for Geomatics** -- GIS, remote sensing, and surveying workflows that are fast, reliable, reproducible, and easy to install.

SudaPy is designed for Sudanese GIS professionals who need a single toolkit that works on Windows, handles common coordinate systems used in Sudan, and provides both a Python API and a friendly command-line interface.

## Features

- Built-in CRS presets for Sudan (WGS 84 UTM 34-37N, Adindan UTM 35-37N)
- Vector operations: reproject, clip, dissolve, area, buffer, simplify, fix-geometry
- Raster operations: clip, reproject, resample, mosaic, hillshade, slope
- Quick map export (PNG or interactive HTML)
- Project scaffolding (`sudapy init`), batch processing, and data reporting
- Environment diagnostics (`sudapy doctor`)
- Remote sensing helpers (Sentinel search/download) via optional extras
- Offline-friendly installation support
- Modern Python packaging with optional extras

## Installation

### From PyPI (recommended)

```bash
# Core (CRS tools, CLI scaffolding, doctor) -- works everywhere, no GDAL needed
pip install sudapy

# Core + vector/raster operations (needs GDAL C libraries)
pip install "sudapy[geo]"

# Core + geo + visualization (matplotlib, folium, contextily)
pip install "sudapy[viz]"

# Everything (geo + viz + remote sensing)
pip install "sudapy[all]"
```

> **Windows note:** The `[geo]` extra requires GDAL C libraries. If `pip install "sudapy[geo]"` fails, use conda to install the geospatial stack first (see below). The core `pip install sudapy` always works.

### Using conda for geospatial dependencies (Windows)

```bash
conda create -n sudapy python=3.11
conda activate sudapy
conda install -c conda-forge geopandas rasterio fiona pyproj
pip install "sudapy[all]"
```

An `environment.yml` is included in the repository for a known-good conda environment:

```bash
conda env create -f environment.yml
conda activate sudapy
```

### Offline installation

See [Offline Installation Guide](https://github.com/Osman-Geomatics93/sudapy/blob/main/INSTALL_OFFLINE.md) for instructions on installing SudaPy without internet access.

## Quickstart

### 1. Check your environment

```bash
sudapy doctor
```

### 2. Find the right CRS for a location in Sudan

```bash
# What UTM zone covers Khartoum?
sudapy crs suggest --lon 32.5 --lat 15.6
```

### 3. Reproject a vector file

```bash
sudapy vector reproject --in data/regions.gpkg --out data/regions_utm.gpkg --to 32636
```

### 4. Calculate area

```bash
sudapy vector area --in data/parcels.gpkg --field area_m2 --out data/parcels_area.gpkg
```

### 5. Quick map

```bash
# Static PNG
sudapy map quick --in data/regions.gpkg --out map.png

# Interactive HTML
sudapy map quick --in data/regions.gpkg --out map.html
```

### 6. Scaffold a new project

```bash
sudapy init my_survey_project
```

### 7. Get a report on a dataset

```bash
sudapy report --in data/parcels.gpkg
```

## Python API

```python
from sudapy.crs.registry import suggest_utm_zone, list_presets
from sudapy.vector.ops import reproject, calculate_area, clip, dissolve, buffer, simplify

# Suggest CRS for a point
suggestions = suggest_utm_zone(lon=32.5, lat=15.6)

# Reproject a file
gdf = reproject("input.gpkg", to_epsg=32636, out="output.gpkg")

# Calculate area with automatic UTM projection
gdf = calculate_area("parcels.gpkg", field="area_m2", out="parcels_area.gpkg")

# Buffer with meters (auto-projects if CRS is geographic)
gdf = buffer("points.gpkg", distance_m=500, out="buffered.gpkg")
```

## Project Structure

```
src/sudapy/
    __init__.py
    core/
        logging.py      # Rich-based logging
        errors.py       # Custom exceptions with hints
    cli/
        main.py         # Typer CLI application
    crs/
        registry.py     # Sudan CRS presets and UTM suggestion
    vector/
        ops.py          # Vector geoprocessing
    raster/
        ops.py          # Raster geoprocessing
    viz/
        maps.py         # Quick map visualization
    rs/
        sentinel.py     # Sentinel satellite search & download
```

## Development

```bash
git clone https://github.com/Osman-Geomatics93/sudapy.git
cd sudapy
pip install -e ".[dev,all]"
pytest
ruff check src/ tests/
```

## Changelog

See [CHANGELOG.md](https://github.com/Osman-Geomatics93/sudapy/blob/main/CHANGELOG.md) for release history.

## License

MIT
