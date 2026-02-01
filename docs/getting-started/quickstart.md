# Quickstart

This guide walks through the most common SudaPy workflows in five minutes.

## 1. Check your environment

```bash
sudapy doctor
```

If any checks fail, see the [Installation](installation.md) page for troubleshooting.

## 2. List available CRS presets

```bash
sudapy crs list
```

Output:

| EPSG  | Name                    | Region                     |
|-------|-------------------------|----------------------------|
| 4326  | WGS 84                  | Global                     |
| 32634 | WGS 84 / UTM zone 34N  | Western Sudan              |
| 32635 | WGS 84 / UTM zone 35N  | Central Sudan              |
| 32636 | WGS 84 / UTM zone 36N  | Eastern Sudan              |
| 32637 | WGS 84 / UTM zone 37N  | Red Sea / Far-Eastern Sudan|
| 20135 | Adindan / UTM zone 35N  | Central Sudan (legacy)     |
| 20136 | Adindan / UTM zone 36N  | Eastern Sudan (legacy)     |
| 20137 | Adindan / UTM zone 37N  | Red Sea (legacy)           |

## 3. Suggest the right CRS for a coordinate

```bash
sudapy crs suggest --lon 32.5 --lat 15.6
```

This returns the WGS 84 UTM zone plus any matching Adindan legacy zone.

## 4. Reproject a vector file

```bash
sudapy vector reproject --in data/regions.gpkg --out data/regions_utm.gpkg --to 32636
```

## 5. Calculate area in square meters

```bash
sudapy vector area --in data/parcels.gpkg --field area_m2 --out data/parcels_area.gpkg
```

!!! note
    If the input CRS is geographic (lat/lon), SudaPy auto-projects to the estimated UTM zone for accurate metric area.

## 6. Create a quick map

=== "Static PNG"

    ```bash
    sudapy map quick --in data/regions.gpkg --out map.png
    ```

=== "Interactive HTML"

    ```bash
    sudapy map quick --in data/regions.gpkg --out map.html
    ```

## 7. Python API

```python
from sudapy.crs.registry import suggest_utm_zone
from sudapy.vector.ops import reproject, calculate_area, buffer

# Find the right zone
suggestions = suggest_utm_zone(lon=32.5, lat=15.6)
print(suggestions[0]["epsg"])  # 32636

# Reproject
gdf = reproject("input.gpkg", to_epsg=32636, out="output.gpkg")

# Calculate area
gdf = calculate_area("parcels.gpkg", field="area_m2", out="parcels_area.gpkg")

# Buffer by 500 meters (auto-projects if geographic CRS)
gdf = buffer("points.gpkg", distance_m=500, out="buffered.gpkg")
```

## Next steps

- [CRS & Coordinate Systems Guide](../guide/crs.md) -- deep dive into Sudan CRS
- [Vector Operations Guide](../guide/vector.md) -- all vector geoprocessing
- [Raster Operations Guide](../guide/raster.md) -- raster processing workflows
- [CLI Reference](../cli.md) -- complete command-line reference
