# Offline Installation

SudaPy supports installation in environments without internet access. This is useful for field work or restricted networks common in surveying and government contexts.

## Strategy overview

| Method | Best for | Complexity |
|--------|----------|------------|
| Wheelhouse (pip) | Pure Python + pre-built wheels | Low |
| conda pack | Full environment with C libraries | Medium |

## Method 1: Wheelhouse (pip)

### On a machine with internet

```bash
# Clone and build the wheelhouse
git clone https://github.com/Osman-Geomatics93/sudapy.git
cd sudapy
python scripts/build_wheelhouse.py
```

This downloads all wheels into a `wheelhouse/` directory. Copy the entire `wheelhouse/` folder to a USB drive.

### On the offline machine

```bash
pip install --no-index --find-links=wheelhouse/ sudapy
```

!!! warning
    Pip wheelhouses work best when the online and offline machines have the **same OS and Python version**. For geospatial C libraries (GDAL, PROJ), conda is more reliable.

## Method 2: conda environment

### On a machine with internet

```bash
# Create and export the environment
conda env create -f environment.yml
conda activate sudapy

# Pack the environment for transfer
conda install -c conda-forge conda-pack
conda pack -n sudapy -o sudapy-env.tar.gz
```

### On the offline machine

```bash
# Unpack
mkdir -p ~/envs/sudapy
tar -xzf sudapy-env.tar.gz -C ~/envs/sudapy

# Activate
source ~/envs/sudapy/bin/activate   # Linux/macOS
# or
~/envs/sudapy/Scripts/activate.bat  # Windows

# Fix prefixes
conda-unpack
```

## Verify offline installation

```bash
sudapy doctor
sudapy info
sudapy crs list
```

All three commands should work without network access since they use only local data.
