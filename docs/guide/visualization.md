# Visualization

SudaPy provides a `quick_map` function for fast visualization of vector and raster data. Output formats include static PNG images and interactive HTML maps.

!!! note "Optional dependency"
    Visualization requires the `viz` extra: `pip install "sudapy[viz]"`

## Quick map export

### Static PNG

=== "CLI"

    ```bash
    sudapy map quick --in regions.gpkg --out map.png
    ```

=== "Python"

    ```python
    from sudapy.viz.maps import quick_map

    quick_map("regions.gpkg", "map.png")
    ```

Generates a 150 DPI image using matplotlib.

### Interactive HTML

=== "CLI"

    ```bash
    sudapy map quick --in regions.gpkg --out map.html
    ```

=== "Python"

    ```python
    from sudapy.viz.maps import quick_map

    quick_map("regions.gpkg", "map.html", title="Sudan Regions")
    ```

Generates a Leaflet map using folium with OpenStreetMap basemap and layer controls.

## Supported input types

| Input type | PNG output | HTML output |
|------------|-----------|-------------|
| Vector (`.gpkg`, `.shp`, `.geojson`) | Matplotlib plot | Folium GeoJSON overlay |
| Raster (`.tif`, `.tiff`, `.img`) | rasterio plot | Bounds rectangle on map |

## Output format selection

The output format is determined by the file extension:

- `.png`, `.jpg` -- static image via matplotlib
- `.html` -- interactive Leaflet map via folium

## Combining with other operations

A common workflow is to process data then visualize:

```python
from sudapy.vector.ops import clip, calculate_area
from sudapy.viz.maps import quick_map

# Process
gdf = clip("parcels.gpkg", "city_boundary.gpkg", out="city_parcels.gpkg")
gdf = calculate_area(gdf, field="area_m2", out="city_parcels_area.gpkg")

# Visualize
quick_map("city_parcels_area.gpkg", "city_parcels.html", title="City Parcels")
quick_map("city_parcels_area.gpkg", "city_parcels.png")
```
