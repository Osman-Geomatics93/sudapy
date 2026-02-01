"""Vector geoprocessing operations.

All functions accept and return :class:`geopandas.GeoDataFrame` objects and
support GeoPackage, GeoJSON, and Shapefile formats on disk.
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Union

from sudapy.core.errors import CRSError, FileFormatError, SudaPyError, require_extra
from sudapy.core.logging import get_logger
from sudapy.crs.registry import validate_epsg

logger = get_logger(__name__)

PathLike = Union[str, Path]

# Supported write drivers keyed by suffix.
_DRIVERS: dict[str, str] = {
    ".gpkg": "GPKG",
    ".geojson": "GeoJSON",
    ".json": "GeoJSON",
    ".shp": "ESRI Shapefile",
}


def _read(path: PathLike):
    gpd = require_extra("geopandas", "geo")
    path = Path(path)
    if not path.exists():
        raise FileFormatError(f"File not found: {path}")
    try:
        return gpd.read_file(path)
    except Exception as exc:
        raise FileFormatError(
            f"Cannot read vector file: {path}",
            hint="Supported formats: GeoPackage (.gpkg), GeoJSON, Shapefile (.shp).",
        ) from exc


def _write(gdf, path: PathLike) -> Path:
    path = Path(path)
    suffix = path.suffix.lower()
    driver = _DRIVERS.get(suffix)
    if driver is None:
        raise FileFormatError(
            f"Unsupported output format '{suffix}'",
            hint=f"Use one of: {', '.join(_DRIVERS.keys())}",
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(path, driver=driver)
    logger.info("Wrote %d features to %s", len(gdf), path)
    return path


def _ensure_projected(gdf):
    """Return a projected copy if the CRS is geographic, else return as-is."""
    if gdf.crs is None:
        raise CRSError(
            "Input dataset has no CRS.",
            hint="Set a CRS first, e.g. 'sudapy vector reproject --in file --out file --to 32635'.",
        )
    if gdf.crs.is_geographic:
        return gdf.to_crs(gdf.estimate_utm_crs())
    return gdf


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def reproject(
    src: PathLike | gpd.GeoDataFrame,
    to_epsg: int,
    out: PathLike | None = None,
) -> gpd.GeoDataFrame:
    """Reproject a vector dataset to a new CRS.

    Args:
        src: Input file path or GeoDataFrame.
        to_epsg: Target EPSG code.
        out: Optional output file path. If given the result is also saved.

    Returns:
        Reprojected GeoDataFrame.
    """
    gpd = require_extra("geopandas", "geo")
    gdf = _read(src) if not isinstance(src, gpd.GeoDataFrame) else src
    target_crs = validate_epsg(to_epsg)
    result = gdf.to_crs(target_crs)
    if out is not None:
        _write(result, out)
    return result


def clip(
    src: PathLike | gpd.GeoDataFrame,
    clip_src: PathLike | gpd.GeoDataFrame,
    out: PathLike | None = None,
) -> gpd.GeoDataFrame:
    """Clip a vector dataset by another vector geometry.

    Args:
        src: Input file or GeoDataFrame.
        clip_src: Clipping geometry file or GeoDataFrame.
        out: Optional output path.

    Returns:
        Clipped GeoDataFrame.
    """
    gpd = require_extra("geopandas", "geo")
    gdf = _read(src) if not isinstance(src, gpd.GeoDataFrame) else src
    mask = _read(clip_src) if not isinstance(clip_src, gpd.GeoDataFrame) else clip_src

    # Ensure same CRS
    if gdf.crs and mask.crs and gdf.crs != mask.crs:
        logger.info("Reprojecting clip geometry to match input CRS (%s)", gdf.crs)
        mask = mask.to_crs(gdf.crs)

    result = gpd.clip(gdf, mask)
    if out is not None:
        _write(result, out)
    return result


def dissolve(
    src: PathLike | gpd.GeoDataFrame,
    by: str,
    out: PathLike | None = None,
) -> gpd.GeoDataFrame:
    """Dissolve geometries by an attribute field.

    Args:
        src: Input file or GeoDataFrame.
        by: Column name to dissolve on.
        out: Optional output path.

    Returns:
        Dissolved GeoDataFrame.
    """
    gpd = require_extra("geopandas", "geo")
    gdf = _read(src) if not isinstance(src, gpd.GeoDataFrame) else src
    if by not in gdf.columns:
        raise SudaPyError(
            f"Column '{by}' not found in dataset.",
            hint=f"Available columns: {', '.join(gdf.columns.tolist())}",
        )
    result = gdf.dissolve(by=by).reset_index()
    if out is not None:
        _write(result, out)
    return result


def calculate_area(
    src: PathLike | gpd.GeoDataFrame,
    field: str = "area_m2",
    out: PathLike | None = None,
) -> gpd.GeoDataFrame:
    """Calculate geometry area in square meters.

    If the CRS is geographic (lat/lon) a warning is emitted and geometries
    are temporarily projected to the appropriate UTM zone for accurate
    area calculation.

    Args:
        src: Input file or GeoDataFrame.
        field: Name of the new area column.
        out: Optional output path.

    Returns:
        GeoDataFrame with a new area column.
    """
    gpd = require_extra("geopandas", "geo")
    gdf = _read(src) if not isinstance(src, gpd.GeoDataFrame) else src.copy()

    if gdf.crs is None:
        raise CRSError(
            "Input dataset has no CRS.",
            hint="Set a CRS first, e.g. 'sudapy vector reproject --in file --out file --to 32635'.",
        )

    if gdf.crs.is_geographic:
        warnings.warn(
            "Input CRS is geographic (lat/lon). Area will be computed by "
            "temporarily projecting to the estimated UTM zone. For best "
            "accuracy, reproject your data to a projected CRS first.",
            UserWarning,
            stacklevel=2,
        )
        projected = gdf.to_crs(gdf.estimate_utm_crs())
        gdf[field] = projected.geometry.area
    else:
        gdf[field] = gdf.geometry.area

    if out is not None:
        _write(gdf, out)
    return gdf


def buffer(
    src: PathLike | gpd.GeoDataFrame,
    distance_m: float,
    out: PathLike | None = None,
) -> gpd.GeoDataFrame:
    """Buffer geometries by a distance in meters.

    If the CRS is geographic, the data is temporarily projected to the
    estimated UTM zone so the buffer distance is applied in meters.

    Args:
        src: Input file or GeoDataFrame.
        distance_m: Buffer distance in meters.
        out: Optional output path.

    Returns:
        Buffered GeoDataFrame (in original CRS).
    """
    gpd = require_extra("geopandas", "geo")
    gdf = _read(src) if not isinstance(src, gpd.GeoDataFrame) else src
    original_crs = gdf.crs

    if original_crs is None:
        raise CRSError(
            "Input dataset has no CRS.",
            hint="Set a CRS so the buffer distance can be applied in meters.",
        )

    if original_crs.is_geographic:
        warnings.warn(
            "Input CRS is geographic. Temporarily projecting to UTM for "
            "accurate meter-based buffering.",
            UserWarning,
            stacklevel=2,
        )
        projected = gdf.to_crs(gdf.estimate_utm_crs())
        projected["geometry"] = projected.geometry.buffer(distance_m)
        result = projected.to_crs(original_crs)
    else:
        result = gdf.copy()
        result["geometry"] = result.geometry.buffer(distance_m)

    if out is not None:
        _write(result, out)
    return result


def simplify(
    src: PathLike | gpd.GeoDataFrame,
    tolerance_m: float,
    out: PathLike | None = None,
) -> gpd.GeoDataFrame:
    """Simplify geometries to reduce vertex count.

    If the CRS is geographic, the data is temporarily projected to UTM
    so the tolerance is applied in meters.

    Args:
        src: Input file or GeoDataFrame.
        tolerance_m: Simplification tolerance in meters.
        out: Optional output path.

    Returns:
        Simplified GeoDataFrame.
    """
    gpd = require_extra("geopandas", "geo")
    gdf = _read(src) if not isinstance(src, gpd.GeoDataFrame) else src
    original_crs = gdf.crs

    if original_crs and original_crs.is_geographic:
        projected = gdf.to_crs(gdf.estimate_utm_crs())
        projected["geometry"] = projected.geometry.simplify(tolerance_m)
        result = projected.to_crs(original_crs)
    else:
        result = gdf.copy()
        result["geometry"] = result.geometry.simplify(tolerance_m)

    if out is not None:
        _write(result, out)
    return result


def fix_geometry(
    src: PathLike | gpd.GeoDataFrame,
    out: PathLike | None = None,
) -> gpd.GeoDataFrame:
    """Repair invalid geometries using :func:`shapely.validation.make_valid`.

    Args:
        src: Input file or GeoDataFrame.
        out: Optional output path.

    Returns:
        GeoDataFrame with all geometries made valid.
    """
    gpd = require_extra("geopandas", "geo")
    from shapely.validation import make_valid  # noqa: E402

    gdf = _read(src) if not isinstance(src, gpd.GeoDataFrame) else src.copy()

    invalid_count = int((~gdf.geometry.is_valid).sum())
    if invalid_count > 0:
        logger.info("Fixing %d invalid geometries", invalid_count)
        gdf["geometry"] = gdf.geometry.apply(
            lambda g: make_valid(g) if g is not None and not g.is_valid else g
        )
    else:
        logger.info("All geometries are already valid")

    if out is not None:
        _write(gdf, out)
    return gdf
