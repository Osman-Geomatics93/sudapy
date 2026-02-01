# Raster Operations

SudaPy wraps `rasterio` to provide high-level raster processing. Supported input formats: GeoTIFF (`.tif`, `.tiff`), ERDAS Imagine (`.img`), and VRT (`.vrt`).

## Clip by vector

Clip a raster using vector geometries as a mask.

=== "CLI"

    ```bash
    sudapy raster clip --in dem.tif --clip boundary.gpkg --out dem_clipped.tif
    ```

=== "Python"

    ```python
    from sudapy.raster.ops import clip

    clip("dem.tif", "boundary.gpkg", out="dem_clipped.tif")
    ```

The clip vector is automatically reprojected to match the raster CRS if needed.

## Reproject

Reproject a raster to a new coordinate reference system.

=== "CLI"

    ```bash
    sudapy raster reproject --in image.tif --out image_utm.tif --to 32636
    ```

=== "Python"

    ```python
    from sudapy.raster.ops import reproject_raster

    reproject_raster("image.tif", "image_utm.tif", to_epsg=32636)
    ```

## Resample

Change raster resolution by a scale factor.

=== "CLI"

    ```bash
    # Double the resolution
    sudapy raster resample --in image.tif --out image_hires.tif --scale 2.0

    # Use cubic resampling
    sudapy raster resample --in image.tif --out image_hires.tif --scale 2.0 --method cubic
    ```

=== "Python"

    ```python
    from sudapy.raster.ops import resample

    resample("image.tif", "image_hires.tif", scale_factor=2.0, method="bilinear")
    ```

Available resampling methods:

| Method | Description |
|--------|-------------|
| `nearest` | Nearest neighbor (fast, good for categorical data) |
| `bilinear` | Bilinear interpolation (good default for continuous data) |
| `cubic` | Cubic convolution (smooth, best for visual quality) |

## Mosaic

Merge multiple raster tiles from a directory into a single raster.

=== "CLI"

    ```bash
    sudapy raster mosaic --in tiles/ --out merged.tif
    ```

=== "Python"

    ```python
    from sudapy.raster.ops import mosaic

    mosaic("tiles/", "merged.tif")
    ```

All `.tif`, `.tiff`, `.img`, and `.vrt` files in the directory are included.

## Hillshade

Generate a hillshade visualization from a Digital Elevation Model (DEM).

=== "CLI"

    ```bash
    sudapy raster hillshade --in dem.tif --out hillshade.tif

    # Custom sun position
    sudapy raster hillshade --in dem.tif --out hillshade.tif --azimuth 270 --altitude 30
    ```

=== "Python"

    ```python
    from sudapy.raster.ops import hillshade

    hillshade("dem.tif", "hillshade.tif", azimuth=315.0, altitude=45.0)
    ```

Parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `azimuth` | 315.0 | Sun direction in degrees (315 = northwest) |
| `altitude` | 45.0 | Sun angle above horizon in degrees |

## Slope

Calculate slope in degrees from a DEM.

=== "CLI"

    ```bash
    sudapy raster slope --in dem.tif --out slope.tif
    ```

=== "Python"

    ```python
    from sudapy.raster.ops import slope

    slope("dem.tif", "slope.tif")
    ```

The output raster contains slope values in degrees (0 = flat, 90 = vertical).

## Terrain analysis workflow

A common DEM analysis workflow:

```bash
# 1. Clip DEM to study area
sudapy raster clip --in srtm_36n.tif --clip study_area.gpkg --out dem.tif

# 2. Reproject to UTM for accurate measurements
sudapy raster reproject --in dem.tif --out dem_utm.tif --to 32636

# 3. Generate terrain products
sudapy raster hillshade --in dem_utm.tif --out hillshade.tif
sudapy raster slope --in dem_utm.tif --out slope.tif
```
