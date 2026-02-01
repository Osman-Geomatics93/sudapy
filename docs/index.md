---
hide:
  - navigation
---

# SudaPy

**Sudan-focused Python toolkit for Geomatics** -- GIS, remote sensing, and surveying workflows.

<div class="grid cards" markdown>

-   :material-map-marker-radius:{ .lg .middle } **CRS Presets for Sudan**

    ---

    Built-in coordinate reference systems for UTM zones 34--37N (WGS 84 and Adindan) with automatic zone detection.

    [:octicons-arrow-right-24: CRS Guide](guide/crs.md)

-   :material-vector-polygon:{ .lg .middle } **Vector Operations**

    ---

    Reproject, clip, dissolve, buffer, simplify, calculate area, and fix invalid geometries.

    [:octicons-arrow-right-24: Vector Guide](guide/vector.md)

-   :material-grid:{ .lg .middle } **Raster Operations**

    ---

    Clip, reproject, resample, mosaic, hillshade, and slope analysis for raster data.

    [:octicons-arrow-right-24: Raster Guide](guide/raster.md)

-   :material-console:{ .lg .middle } **CLI & Python API**

    ---

    Use SudaPy from the command line or import it as a Python library in your scripts.

    [:octicons-arrow-right-24: CLI Reference](cli.md)

</div>

## Quick Example

=== "CLI"

    ```bash
    # Find the right CRS for Khartoum
    sudapy crs suggest --lon 32.5 --lat 15.6

    # Reproject a vector file
    sudapy vector reproject --in regions.gpkg --out regions_utm.gpkg --to 32636

    # Generate a quick map
    sudapy map quick --in regions.gpkg --out map.html
    ```

=== "Python"

    ```python
    from sudapy.crs.registry import suggest_utm_zone
    from sudapy.vector.ops import reproject, calculate_area

    # Suggest CRS for a point in Sudan
    suggestions = suggest_utm_zone(lon=32.5, lat=15.6)
    print(suggestions)
    # [{'epsg': 32636, 'zone': 36, 'name': 'WGS 84 / UTM zone 36N', ...}]

    # Reproject and calculate area
    gdf = reproject("parcels.gpkg", to_epsg=32636, out="parcels_utm.gpkg")
    gdf = calculate_area(gdf, field="area_m2", out="parcels_area.gpkg")
    ```

## Install

```bash
pip install sudapy
```

For geospatial dependencies on Windows, use conda first:

```bash
conda install -c conda-forge geopandas rasterio fiona pyproj
pip install sudapy
```

[:octicons-arrow-right-24: Full installation guide](getting-started/installation.md)
