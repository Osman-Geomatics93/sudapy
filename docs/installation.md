# Installation

## Requirements

- Python 3.9 or later
- GDAL (via rasterio/fiona) -- easiest to install through conda

## pip install

```bash
pip install sudapy          # Core
pip install "sudapy[viz]"   # + visualization
pip install "sudapy[rs]"    # + remote sensing
pip install "sudapy[all]"   # Everything
```

## conda + pip (recommended for Windows)

```bash
conda create -n sudapy python=3.11
conda activate sudapy
conda install -c conda-forge geopandas rasterio fiona pyproj
pip install sudapy
```

## Offline installation

See [INSTALL_OFFLINE.md](../INSTALL_OFFLINE.md).
