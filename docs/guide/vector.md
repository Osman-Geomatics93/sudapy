# Vector Operations

SudaPy provides a set of vector geoprocessing functions accessible from both the CLI and Python API. All functions accept GeoPackage (`.gpkg`), GeoJSON, and Shapefile (`.shp`) formats.

## Reproject

Change the coordinate reference system of a vector dataset.

=== "CLI"

    ```bash
    sudapy vector reproject --in regions.gpkg --out regions_utm.gpkg --to 32636
    ```

=== "Python"

    ```python
    from sudapy.vector.ops import reproject

    gdf = reproject("regions.gpkg", to_epsg=32636, out="regions_utm.gpkg")
    ```

## Clip

Clip a vector dataset using another geometry as a mask.

=== "CLI"

    ```bash
    sudapy vector clip --in parcels.gpkg --clip boundary.gpkg --out clipped.gpkg
    ```

=== "Python"

    ```python
    from sudapy.vector.ops import clip

    gdf = clip("parcels.gpkg", "boundary.gpkg", out="clipped.gpkg")
    ```

!!! note
    If the clip geometry has a different CRS, SudaPy automatically reprojects it to match the input.

## Dissolve

Merge geometries by an attribute field.

=== "CLI"

    ```bash
    sudapy vector dissolve --in districts.gpkg --by state_name --out states.gpkg
    ```

=== "Python"

    ```python
    from sudapy.vector.ops import dissolve

    gdf = dissolve("districts.gpkg", by="state_name", out="states.gpkg")
    ```

## Calculate area

Add an area column in square meters.

=== "CLI"

    ```bash
    sudapy vector area --in parcels.gpkg --field area_m2 --out parcels_area.gpkg
    ```

=== "Python"

    ```python
    from sudapy.vector.ops import calculate_area

    gdf = calculate_area("parcels.gpkg", field="area_m2", out="parcels_area.gpkg")
    ```

!!! tip "Automatic UTM projection"
    If the input CRS is geographic (lat/lon), SudaPy temporarily projects to the estimated UTM zone for accurate metric area. A warning is emitted. For best accuracy, reproject your data to a projected CRS first.

## Buffer

Create buffer zones around geometries. Distance is specified in meters.

=== "CLI"

    ```bash
    sudapy vector buffer --in wells.gpkg --distance 500 --out wells_buffer.gpkg
    ```

=== "Python"

    ```python
    from sudapy.vector.ops import buffer

    gdf = buffer("wells.gpkg", distance_m=500, out="wells_buffer.gpkg")
    ```

If the input CRS is geographic, SudaPy auto-projects to UTM, applies the buffer in meters, then projects back to the original CRS.

## Simplify

Reduce vertex count using the Douglas-Peucker algorithm. Tolerance is in meters.

=== "CLI"

    ```bash
    sudapy vector simplify --in detailed.gpkg --tolerance 100 --out simplified.gpkg
    ```

=== "Python"

    ```python
    from sudapy.vector.ops import simplify

    gdf = simplify("detailed.gpkg", tolerance_m=100, out="simplified.gpkg")
    ```

## Fix geometry

Repair invalid geometries using Shapely's `make_valid`.

=== "CLI"

    ```bash
    sudapy vector fix-geometry --in broken.gpkg --out fixed.gpkg
    ```

=== "Python"

    ```python
    from sudapy.vector.ops import fix_geometry

    gdf = fix_geometry("broken.gpkg", out="fixed.gpkg")
    ```

!!! tip
    Run `sudapy report --in file.gpkg` first to check how many invalid geometries exist before fixing.

## Supported formats

| Extension | Format | Read | Write |
|-----------|--------|------|-------|
| `.gpkg` | GeoPackage | Yes | Yes |
| `.geojson` / `.json` | GeoJSON | Yes | Yes |
| `.shp` | ESRI Shapefile | Yes | Yes |

## Working with GeoDataFrames directly

All functions accept either a file path or a `geopandas.GeoDataFrame`. The `out` parameter is optional -- omit it to get the result in memory without writing to disk:

```python
import geopandas as gpd
from sudapy.vector.ops import buffer, calculate_area

gdf = gpd.read_file("parcels.gpkg")

# Chain operations in memory
gdf = calculate_area(gdf, field="area_m2")
gdf = buffer(gdf, distance_m=100)

# Write only at the end
gdf.to_file("result.gpkg", driver="GPKG")
```
