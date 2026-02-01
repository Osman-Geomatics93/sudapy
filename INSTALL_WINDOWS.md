# Windows Installation Guide

Four ways to install SudaPy on Windows, from simplest to most flexible.

---

## Option 1: Portable Windows Bundle (Recommended)

No Python, pip, conda, or Visual Studio required. Everything is included.

1. Go to the [latest release](https://github.com/Osman-Geomatics93/sudapy/releases/latest)
2. Download **SudaPy-Windows-x64.zip** (~600 MB)
3. Extract to a short path, e.g. `C:\SudaPy`
4. Open Command Prompt and run:

```bat
cd C:\SudaPy
scripts\sudapy_doctor.bat
scripts\run_sudapy.bat crs suggest --lon 32.5 --lat 15.6
```

**Requirements:** Windows 10/11, 64-bit.

> This is also the **offline installer** -- copy the zip to a USB drive, transfer to an air-gapped machine, extract, and run.

---

## Option 2: pip Core-Only (No Geo Features)

If you only need CRS tools, the CLI scaffolding, and `sudapy doctor`:

```bash
pip install sudapy
```

This works on any platform without GDAL. Vector/raster/visualization commands will show a message asking you to install the `[geo]` extra.

---

## Option 3: conda + pip Hybrid (Full Features)

Use conda to install the geospatial C libraries, then pip for SudaPy:

```bash
conda create -n sudapy python=3.11
conda activate sudapy
conda install -c conda-forge geopandas rasterio fiona pyproj scipy
pip install "sudapy[all]"
```

---

## Option 4: environment.yml (Developer Setup)

Clone the repository and create the full environment from the lock file:

```bash
git clone https://github.com/Osman-Geomatics93/sudapy.git
cd sudapy
conda env create -f environment.yml
conda activate sudapy
pip install -e ".[dev]"
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `pip install "sudapy[geo]"` fails with build errors | Use Option 1 (bundle) or Option 3 (conda) instead |
| Bundle says "Cannot find bundled Python" | Extract the full zip -- avoid very long paths |
| Antivirus flags the bundle | Add the SudaPy folder to your exclusion list |
| 32-bit Python warning | SudaPy core works on 32-bit, but geo extras need 64-bit Python |

For more help, open an [issue on GitHub](https://github.com/Osman-Geomatics93/sudapy/issues).
