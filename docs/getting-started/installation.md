# Installation

## Requirements

- Python 3.9 or later
- GDAL C libraries are **only** needed for vector/raster operations (the `[geo]` extra)

!!! tip "Windows users"
    The core `pip install sudapy` works everywhere -- no GDAL needed. For vector/raster support, install the `[geo]` extra. If `pip install "sudapy[geo]"` fails on Windows, use **conda** to install binary dependencies first (see below).

## From PyPI

```bash
# Core (CRS tools, CLI scaffolding, doctor) -- works everywhere
pip install sudapy

# Core + vector/raster operations (needs GDAL C libraries)
pip install "sudapy[geo]"

# Core + geo + visualization (matplotlib, folium, contextily)
pip install "sudapy[viz]"

# With remote-sensing extras (earthpy, sentinelsat)
pip install "sudapy[rs]"

# Everything (geo + viz + rs)
pip install "sudapy[all]"
```

### What works without `[geo]`

After `pip install sudapy` (no extras), you can use:

- `sudapy crs list` / `sudapy crs suggest` -- CRS tools
- `sudapy doctor` / `sudapy info` -- environment diagnostics
- `sudapy init` -- project scaffolding
- Python API: `from sudapy.crs.registry import suggest_utm_zone`

Vector, raster, visualization, and reporting commands require `pip install "sudapy[geo]"`.

## Using conda (recommended for Windows with `[geo]`)

Create a clean environment with the geospatial stack, then install SudaPy on top:

```bash
conda create -n sudapy python=3.11
conda activate sudapy
conda install -c conda-forge geopandas rasterio fiona pyproj shapely
pip install "sudapy[all]"
```

A ready-made `environment.yml` is included in the repository:

```bash
git clone https://github.com/Osman-Geomatics93/sudapy.git
cd sudapy
conda env create -f environment.yml
conda activate sudapy
```

## Verify the installation

After installing, run the built-in diagnostics:

```bash
sudapy doctor
```

This checks Python version, core imports (pyproj, pandas), and optionally geo imports (geopandas, shapely, rasterio, fiona). Missing optional dependencies show as `SKIP` (yellow) rather than `FAIL`.

Expected output with core-only install:

```
┌──────────────────────────────────────────────────────────┐
│                      SudaPy Doctor                       │
├───────────────────────────────┬────────┬─────────────────┤
│ Check                         │ Status │ Details         │
├───────────────────────────────┼────────┼─────────────────┤
│ Python >= 3.9                 │ PASS   │ 3.11.x          │
│ pyproj import                 │ PASS   │ OK              │
│ pandas import                 │ PASS   │ OK              │
│ PROJ data available           │ PASS   │ OK (WGS 84 ..) │
│ geopandas import (optional)   │ SKIP   │ not installed   │
│ shapely import (optional)     │ SKIP   │ not installed   │
│ ...                           │        │                 │
└───────────────────────────────┴────────┴─────────────────┘
Core checks passed. Install geo extras for vector/raster support: pip install "sudapy[geo]"
```

## Development install

To contribute or hack on SudaPy itself:

```bash
git clone https://github.com/Osman-Geomatics93/sudapy.git
cd sudapy
pip install -e ".[dev,all]"
pytest
ruff check src/ tests/
```

## Optional extras reference

| Extra | Packages added | Use case |
|-------|---------------|----------|
| `geo` | geopandas, shapely, fiona, rasterio, numpy | Vector/raster operations (needs GDAL) |
| `viz` | `geo` + matplotlib, folium, contextily | Map visualization (PNG/HTML) |
| `rs` | earthpy, sentinelsat | Sentinel satellite search & download |
| `all` | `geo` + `viz` + `rs` | Everything |
| `dev` | pytest, pytest-cov, ruff, mypy | Development & testing |
