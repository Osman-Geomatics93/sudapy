# Installation

## Requirements

- Python 3.9 or later
- GDAL (provided automatically by `rasterio` and `fiona`)

!!! tip "Windows users"
    Geospatial C libraries (GDAL, PROJ, GEOS) can be difficult to compile from source on Windows. Using **conda** to install binary dependencies first is strongly recommended.

## From PyPI

```bash
# Core toolkit
pip install sudapy

# With visualization extras (matplotlib, folium, contextily)
pip install "sudapy[viz]"

# With remote-sensing extras (earthpy, sentinelsat)
pip install "sudapy[rs]"

# Everything
pip install "sudapy[all]"
```

## Using conda (recommended for Windows)

Create a clean environment with the geospatial stack, then install SudaPy on top:

```bash
conda create -n sudapy python=3.11
conda activate sudapy
conda install -c conda-forge geopandas rasterio fiona pyproj shapely
pip install sudapy
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

This checks Python version, core imports (geopandas, shapely, pyproj, rasterio, fiona), PROJ data availability, and GeoPackage read/write support.

Expected output when everything is working:

```
┌──────────────────────────────────────────────────┐
│                  SudaPy Doctor                   │
├─────────────────────┬────────┬───────────────────┤
│ Check               │ Status │ Details           │
├─────────────────────┼────────┼───────────────────┤
│ Python >= 3.9       │ PASS   │ 3.11.x            │
│ geopandas import    │ PASS   │ OK                │
│ shapely import      │ PASS   │ OK                │
│ pyproj import       │ PASS   │ OK                │
│ rasterio import     │ PASS   │ OK (GDAL x.y.z)   │
│ fiona import        │ PASS   │ OK                │
│ PROJ data available │ PASS   │ OK (WGS 84 ...)   │
│ GeoPackage r/w      │ PASS   │ OK                │
└─────────────────────┴────────┴───────────────────┘
All checks passed. SudaPy is ready.
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
| `viz` | matplotlib, folium, contextily | Map visualization (PNG/HTML) |
| `rs` | earthpy, sentinelsat | Sentinel satellite search & download |
| `all` | `viz` + `rs` | Everything |
| `dev` | pytest, pytest-cov, ruff, mypy | Development & testing |
