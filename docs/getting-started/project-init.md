# Project Scaffolding

SudaPy includes a project scaffolding command that creates a standardized folder structure for geomatics projects.

## Create a new project

```bash
sudapy init my_survey_project
```

This creates the following structure:

```
my_survey_project/
    README.md
    data_raw/          # Original source data (do not modify)
    data_clean/        # Cleaned / processed data
    outputs/           # Analysis results, tables, statistics
    maps/              # Exported maps (PNG, HTML)
    scripts/
        process.py     # Starter processing script
```

## Folder conventions

| Folder | Purpose |
|--------|---------|
| `data_raw/` | Store original datasets here. Treat this as read-only to preserve data provenance. |
| `data_clean/` | Processed, cleaned, or reprojected data ready for analysis. |
| `outputs/` | Analysis results: CSVs, statistics, exported tables. |
| `maps/` | Generated map images (PNG) and interactive maps (HTML). |
| `scripts/` | Python processing scripts. A starter `process.py` is included. |

## The starter script

The generated `scripts/process.py` contains a minimal template:

```python
"""Processing script -- edit this for your workflow."""

from sudapy.crs.registry import suggest_utm_zone
from sudapy.vector.ops import reproject

# Example: suggest CRS for Khartoum
print(suggest_utm_zone(lon=32.5, lat=15.6))
```

Edit this file to build your processing pipeline.

## Typical workflow

```bash
# 1. Create project
sudapy init khartoum_analysis

cd khartoum_analysis

# 2. Copy raw data
cp ~/Downloads/parcels.gpkg data_raw/

# 3. Process
sudapy vector reproject --in data_raw/parcels.gpkg --out data_clean/parcels_utm.gpkg --to 32636
sudapy vector area --in data_clean/parcels_utm.gpkg --field area_m2 --out data_clean/parcels_area.gpkg

# 4. Generate report
sudapy report --in data_clean/parcels_area.gpkg

# 5. Export map
sudapy map quick --in data_clean/parcels_area.gpkg --out maps/parcels.html
```
