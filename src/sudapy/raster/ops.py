"""Raster geoprocessing operations.

Functions wrap :mod:`rasterio` to provide high-level raster processing
capabilities: clip, reproject, resample, mosaic, hillshade, and slope.
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

from sudapy.core.errors import FileFormatError, SudaPyError, require_extra
from sudapy.core.logging import get_logger
from sudapy.crs.registry import validate_epsg

logger = get_logger(__name__)

PathLike = Union[str, Path]

_RASTER_EXTS = {".tif", ".tiff", ".img", ".vrt"}


def clip(
    src: PathLike,
    clip_vector: PathLike,
    out: PathLike,
    *,
    crop: bool = True,
    nodata: float | None = None,
) -> Path:
    """Clip a raster by vector geometries.

    Args:
        src: Input raster path.
        clip_vector: Vector file whose geometries define the clip extent.
        out: Output raster path.
        crop: Whether to crop the raster extent to the vector bounds.
        nodata: NoData value for masked pixels. Defaults to the source nodata.

    Returns:
        Path to the output raster.
    """
    rasterio = require_extra("rasterio", "geo")
    import rasterio.mask

    from sudapy.vector.ops import _read as read_vector

    src = Path(src)
    out = Path(out)
    if not src.exists():
        raise FileFormatError(f"Raster not found: {src}")

    mask_gdf = read_vector(clip_vector)

    with rasterio.open(src) as ds:
        if mask_gdf.crs and mask_gdf.crs != ds.crs:
            logger.info("Reprojecting clip vector to raster CRS (%s)", ds.crs)
            mask_gdf = mask_gdf.to_crs(ds.crs)

        geometries = mask_gdf.geometry.values
        nd = nodata if nodata is not None else ds.nodata

        out_image, out_transform = rasterio.mask.mask(
            ds, geometries, crop=crop, nodata=nd,
        )
        out_meta = ds.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "nodata": nd,
        })

    out.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(out, "w", **out_meta) as dst:
        dst.write(out_image)

    logger.info("Clipped raster written to %s", out)
    return out


def reproject_raster(
    src: PathLike,
    out: PathLike,
    to_epsg: int,
    *,
    resampling: str = "nearest",
) -> Path:
    """Reproject a raster to a new CRS.

    Args:
        src: Input raster path.
        out: Output raster path.
        to_epsg: Target EPSG code.
        resampling: Resampling method name: ``nearest``, ``bilinear``, ``cubic``.

    Returns:
        Path to the output raster.
    """
    rasterio = require_extra("rasterio", "geo")
    from rasterio.warp import Resampling, calculate_default_transform
    from rasterio.warp import reproject as rio_reproject

    _resampling_map = {
        "nearest": Resampling.nearest,
        "bilinear": Resampling.bilinear,
        "cubic": Resampling.cubic,
    }
    resampling_method = _resampling_map.get(resampling)
    if resampling_method is None:
        raise SudaPyError(
            f"Unknown resampling method '{resampling}'",
            hint=f"Supported: {', '.join(_resampling_map.keys())}",
        )

    src = Path(src)
    out = Path(out)
    if not src.exists():
        raise FileFormatError(f"Raster not found: {src}")

    dst_crs = validate_epsg(to_epsg)

    with rasterio.open(src) as ds:
        transform, width, height = calculate_default_transform(
            ds.crs, dst_crs, ds.width, ds.height, *ds.bounds
        )
        kwargs = ds.meta.copy()
        kwargs.update({
            "crs": dst_crs,
            "transform": transform,
            "width": width,
            "height": height,
            "driver": "GTiff",
        })

        out.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(out, "w", **kwargs) as dst:
            for i in range(1, ds.count + 1):
                rio_reproject(
                    source=rasterio.band(ds, i),
                    destination=rasterio.band(dst, i),
                    src_transform=ds.transform,
                    src_crs=ds.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=resampling_method,
                )

    logger.info("Reprojected raster written to %s", out)
    return out


def resample(
    src: PathLike,
    out: PathLike,
    scale_factor: float,
    method: str = "bilinear",
) -> Path:
    """Resample a raster by a scale factor.

    Args:
        src: Input raster path.
        out: Output raster path.
        scale_factor: Factor to scale resolution (2.0 = double resolution).
        method: Resampling method name: ``nearest``, ``bilinear``, ``cubic``.

    Returns:
        Path to the output raster.
    """
    rasterio = require_extra("rasterio", "geo")
    from rasterio.warp import Resampling

    _resampling_map = {
        "nearest": Resampling.nearest,
        "bilinear": Resampling.bilinear,
        "cubic": Resampling.cubic,
    }

    src = Path(src)
    out = Path(out)
    if not src.exists():
        raise FileFormatError(f"Raster not found: {src}")

    resampling_method = _resampling_map.get(method)
    if resampling_method is None:
        raise SudaPyError(
            f"Unknown resampling method '{method}'",
            hint=f"Supported: {', '.join(_resampling_map.keys())}",
        )

    with rasterio.open(src) as ds:
        new_height = int(ds.height * scale_factor)
        new_width = int(ds.width * scale_factor)

        data = ds.read(
            out_shape=(ds.count, new_height, new_width),
            resampling=resampling_method,
        )

        transform = ds.transform * ds.transform.scale(
            ds.width / new_width,
            ds.height / new_height,
        )

        kwargs = ds.meta.copy()
        kwargs.update({
            "driver": "GTiff",
            "height": new_height,
            "width": new_width,
            "transform": transform,
        })

    out.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(out, "w", **kwargs) as dst:
        dst.write(data)

    logger.info("Resampled raster (x%.1f, %s) written to %s", scale_factor, method, out)
    return out


def mosaic(
    src_dir: PathLike,
    out: PathLike,
) -> Path:
    """Merge multiple raster tiles from a directory into one.

    Args:
        src_dir: Directory containing raster tiles.
        out: Output merged raster path.

    Returns:
        Path to the merged raster.
    """
    src_dir = Path(src_dir)
    out = Path(out)
    if not src_dir.is_dir():
        raise FileFormatError(f"Not a directory: {src_dir}")

    rasterio = require_extra("rasterio", "geo")
    from rasterio.merge import merge as rio_merge

    raster_files = sorted(
        f for f in src_dir.iterdir() if f.suffix.lower() in _RASTER_EXTS
    )
    if not raster_files:
        raise FileFormatError(
            f"No raster files found in {src_dir}",
            hint=f"Supported extensions: {', '.join(_RASTER_EXTS)}",
        )

    datasets = [rasterio.open(f) for f in raster_files]
    try:
        mosaic_data, mosaic_transform = rio_merge(datasets)
    finally:
        for ds in datasets:
            ds.close()

    kwargs = datasets[0].meta.copy()
    kwargs.update({
        "driver": "GTiff",
        "height": mosaic_data.shape[1],
        "width": mosaic_data.shape[2],
        "transform": mosaic_transform,
    })

    out.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(out, "w", **kwargs) as dst:
        dst.write(mosaic_data)

    logger.info("Mosaic of %d tiles written to %s", len(raster_files), out)
    return out


def hillshade(
    src: PathLike,
    out: PathLike,
    *,
    azimuth: float = 315.0,
    altitude: float = 45.0,
) -> Path:
    """Generate a hillshade from a DEM raster.

    Args:
        src: Input DEM raster path (single band, elevation values).
        out: Output hillshade raster path.
        azimuth: Sun azimuth in degrees (default 315 = northwest).
        altitude: Sun altitude in degrees above horizon (default 45).

    Returns:
        Path to the hillshade raster.
    """
    rasterio = require_extra("rasterio", "geo")
    np = require_extra("numpy", "geo")

    src = Path(src)
    out = Path(out)
    if not src.exists():
        raise FileFormatError(f"Raster not found: {src}")

    with rasterio.open(src) as ds:
        dem = ds.read(1).astype(np.float64)
        cellsize_x = abs(ds.transform.a)
        cellsize_y = abs(ds.transform.e)

        hs = _compute_hillshade(dem, cellsize_x, cellsize_y, azimuth, altitude)

        kwargs = ds.meta.copy()
        kwargs.update({
            "driver": "GTiff",
            "dtype": "float32",
            "count": 1,
        })

    out.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(out, "w", **kwargs) as dst:
        dst.write(hs.astype(np.float32), 1)

    logger.info("Hillshade written to %s", out)
    return out


def slope(
    src: PathLike,
    out: PathLike,
) -> Path:
    """Calculate slope in degrees from a DEM raster.

    Args:
        src: Input DEM raster path (single band).
        out: Output slope raster path (values in degrees).

    Returns:
        Path to the slope raster.
    """
    rasterio = require_extra("rasterio", "geo")
    np = require_extra("numpy", "geo")

    src = Path(src)
    out = Path(out)
    if not src.exists():
        raise FileFormatError(f"Raster not found: {src}")

    with rasterio.open(src) as ds:
        dem = ds.read(1).astype(np.float64)
        cellsize_x = abs(ds.transform.a)
        cellsize_y = abs(ds.transform.e)

        slope_deg = _compute_slope(dem, cellsize_x, cellsize_y)

        kwargs = ds.meta.copy()
        kwargs.update({
            "driver": "GTiff",
            "dtype": "float32",
            "count": 1,
        })

    out.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(out, "w", **kwargs) as dst:
        dst.write(slope_deg.astype(np.float32), 1)

    logger.info("Slope raster written to %s", out)
    return out


# ---------------------------------------------------------------------------
# Internal helpers for terrain analysis
# ---------------------------------------------------------------------------

def _compute_slope(dem, dx: float, dy: float):
    """Compute slope in degrees using numpy gradient."""
    import numpy as np

    grad_y, grad_x = np.gradient(dem, dy, dx)
    slope_rad = np.arctan(np.sqrt(grad_x**2 + grad_y**2))
    return np.degrees(slope_rad)


def _compute_hillshade(
    dem,
    dx: float,
    dy: float,
    azimuth: float,
    altitude: float,
):
    """Compute hillshade illumination values (0-255)."""
    import numpy as np

    az_rad = np.radians(360.0 - azimuth + 90.0)
    alt_rad = np.radians(altitude)

    grad_y, grad_x = np.gradient(dem, dy, dx)
    slope_rad = np.arctan(np.sqrt(grad_x**2 + grad_y**2))
    aspect_rad = np.arctan2(-grad_y, grad_x)

    hs = (
        np.sin(alt_rad) * np.cos(slope_rad)
        + np.cos(alt_rad) * np.sin(slope_rad) * np.cos(az_rad - aspect_rad)
    )
    hs = np.clip(hs, 0, 1) * 255.0
    return hs
