# Quickstart

## CLI

```bash
# Check environment
sudapy info

# Suggest CRS for Khartoum
sudapy crs suggest --lon 32.5 --lat 15.6

# Reproject a vector file
sudapy vector reproject --in regions.gpkg --out regions_utm.gpkg --to 32636

# Calculate area
sudapy vector area --in parcels.gpkg --field area_m2 --out parcels_area.gpkg
```

## Python API

```python
from sudapy.crs.registry import suggest_utm_zone
from sudapy.vector.ops import reproject, calculate_area

suggestions = suggest_utm_zone(lon=32.5, lat=15.6)
print(suggestions)

gdf = reproject("input.gpkg", to_epsg=32636)
gdf = calculate_area(gdf, field="area_m2", out="output.gpkg")
```
