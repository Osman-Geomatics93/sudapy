# Offline Installation Guide

This guide explains how to install SudaPy on a Windows machine without internet access.

## Overview

The strategy is:

1. On a machine **with** internet, download all wheel files into a local folder (a "wheelhouse").
2. Copy that folder to the offline machine via USB drive, shared folder, etc.
3. Install from the wheelhouse using `pip install --no-index`.

## Step 1: Build the wheelhouse (on a connected machine)

Make sure you have Python 3.9+ and pip installed.

```bash
# Clone or download the SudaPy source
cd sudapy

# Run the wheelhouse builder script
python scripts/build_wheelhouse.py --out wheelhouse/
```

This downloads SudaPy and all its dependencies as `.whl` files into the `wheelhouse/` folder.

Alternatively, build manually:

```bash
pip download "sudapy[all]" --dest wheelhouse/
# Or from the local source:
pip wheel . --wheel-dir wheelhouse/ --no-deps
pip download -r requirements-offline.txt --dest wheelhouse/
```

## Step 2: Transfer to the offline machine

Copy the entire `wheelhouse/` folder and the SudaPy source to the target machine. Use a USB drive, network share, or any other transfer method.

## Step 3: Install on the offline machine

```bash
# Install SudaPy and all dependencies from the wheelhouse
pip install --no-index --find-links wheelhouse/ sudapy

# Or with extras
pip install --no-index --find-links wheelhouse/ "sudapy[all]"
```

## Alternative: conda/mamba approach

If you prefer conda, the geospatial stack can be pre-packaged:

```bash
# On the connected machine:
conda create -n sudapy python=3.11 geopandas rasterio fiona pyproj -c conda-forge
conda activate sudapy

# Export the environment
conda list --explicit > spec-file.txt

# On the offline machine (after transferring the conda packages):
conda create -n sudapy --file spec-file.txt --offline
conda activate sudapy
pip install --no-index --find-links wheelhouse/ sudapy
```

### Tradeoffs: pip wheelhouse vs. conda

| Aspect | pip wheelhouse | conda |
|---|---|---|
| Binary deps (GDAL) | May need pre-built wheels or build tools | Handles binary deps natively |
| Package size | Smaller (Python-only wheels) | Larger (includes C libraries) |
| Setup complexity | Simpler for pure Python | More steps but more reliable for geospatial |
| Reproducibility | Good with pinned versions | Excellent with explicit spec files |

**Recommendation for Sudan/Windows users:** Use conda to install the geospatial binary dependencies (GDAL, rasterio, fiona), then use a pip wheelhouse for SudaPy itself. This gives the most reliable experience on Windows without needing a C compiler.

## Troubleshooting

- **"No matching distribution found"**: Ensure the wheelhouse was built for the same Python version and OS as the target machine.
- **GDAL/rasterio build errors**: Use conda for geospatial deps, then pip for SudaPy.
- **Permission errors on Windows**: Run the terminal as Administrator, or use `--user` flag with pip.
