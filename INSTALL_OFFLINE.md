# Offline Installation Guide

How to install SudaPy on a machine without internet access.

---

## Option 1: Portable Windows Bundle (Recommended)

The simplest offline method. No Python, pip, or conda needed on the target machine.

1. On a connected machine, download **SudaPy-Windows-x64.zip** from the [latest release](https://github.com/Osman-Geomatics93/sudapy/releases/latest)
2. Copy the zip to the offline machine via USB drive, network share, etc.
3. Extract to a short path, e.g. `C:\SudaPy`
4. Open Command Prompt and run:

```bat
cd C:\SudaPy
scripts\sudapy_doctor.bat
scripts\run_sudapy.bat crs suggest --lon 32.5 --lat 15.6
```

The bundle includes Python, GDAL, PROJ, GEOS, and all dependencies. Nothing else to install.

---

## Option 2: pip Wheelhouse (Core-Only)

For pip-only installs without geospatial extras. Requires Python 3.9+ on the target machine.

### On a connected machine

```bash
# Download SudaPy and all core dependencies as wheel files
pip download sudapy --dest wheelhouse/
```

### Transfer

Copy the `wheelhouse/` folder to the offline machine via USB drive or network share.

### On the offline machine

```bash
pip install --no-index --find-links wheelhouse/ sudapy
```

> **Note:** This method only supports the core package (`pip install sudapy`). The `[geo]` extra requires compiled C libraries (GDAL, PROJ, GEOS) that cannot be reliably installed from wheels on Windows. Use Option 1 for full geospatial support offline.

---

## Comparison

| Aspect | Portable Bundle | pip Wheelhouse |
|---|---|---|
| Geospatial support | Full (GDAL, rasterio, fiona, geopandas) | Core only (CRS, CLI) |
| Target requirements | Windows 10/11, 64-bit | Python 3.9+ |
| Download size | ~600 MB | ~20 MB |
| Setup steps | Extract zip, run | pip install from folder |

**Recommendation:** Use the portable bundle for Windows machines that need geospatial functionality. Use the wheelhouse for lightweight core-only installs or non-Windows systems.

---

## Troubleshooting

- **"No matching distribution found"**: Ensure the wheelhouse was built for the same Python version and OS as the target machine.
- **Bundle "Cannot find bundled Python"**: Extract the full zip to a short path (e.g. `C:\SudaPy`).
- **Permission errors on Windows**: Run the terminal as Administrator, or use `--user` flag with pip.
