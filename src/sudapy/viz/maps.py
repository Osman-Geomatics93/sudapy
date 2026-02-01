"""Quick map visualization helpers.

Supports exporting vector or raster data to PNG (static) or HTML (interactive).
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

from sudapy.core.errors import FileFormatError, check_import, require_extra
from sudapy.core.logging import get_logger

logger = get_logger(__name__)

PathLike = Union[str, Path]

_RASTER_EXTS = {".tif", ".tiff", ".img", ".vrt"}
_VECTOR_EXTS = {".gpkg", ".geojson", ".json", ".shp"}


def _is_raster(path: Path) -> bool:
    return path.suffix.lower() in _RASTER_EXTS


def _is_vector(path: Path) -> bool:
    return path.suffix.lower() in _VECTOR_EXTS


def quick_map(
    src: PathLike,
    out: PathLike,
    *,
    title: str | None = None,
) -> Path:
    """Create a quick visualization of a vector or raster dataset.

    The output format is determined by the extension of *out*:

    - ``.png`` / ``.jpg`` - static image (requires matplotlib).
    - ``.html`` - interactive Leaflet map (requires folium).

    Args:
        src: Input vector or raster file path.
        out: Output image/HTML path.
        title: Optional title for the map.

    Returns:
        Path to the generated output.
    """
    src = Path(src)
    out = Path(out)
    if not src.exists():
        raise FileFormatError(f"Input file not found: {src}")

    out.parent.mkdir(parents=True, exist_ok=True)

    if out.suffix.lower() == ".html":
        return _export_html(src, out, title=title)
    else:
        return _export_static(src, out, title=title)


def _export_static(src: Path, out: Path, *, title: str | None = None) -> Path:
    check_import("matplotlib", extra="viz")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    if _is_vector(src):
        gpd = require_extra("geopandas", "geo")
        gdf = gpd.read_file(src)
        gdf.plot(ax=ax, edgecolor="black", linewidth=0.5)
    elif _is_raster(src):
        rasterio = require_extra("rasterio", "geo")
        with rasterio.open(src) as ds:
            from rasterio.plot import show

            show(ds, ax=ax)
    else:
        raise FileFormatError(
            f"Cannot determine type of '{src.name}'",
            hint="Use a recognized vector (.gpkg, .shp, .geojson) or raster (.tif) extension.",
        )

    ax.set_title(title or src.stem)
    ax.set_axis_off()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Static map saved to %s", out)
    return out


def _export_html(src: Path, out: Path, *, title: str | None = None) -> Path:
    check_import("folium", extra="viz")
    import folium

    if _is_vector(src):
        gpd = require_extra("geopandas", "geo")
        gdf = gpd.read_file(src)
        gdf_wgs = gdf.to_crs(4326)
        bounds = gdf_wgs.total_bounds  # minx, miny, maxx, maxy
        center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]

        m = folium.Map(location=center, zoom_start=8, tiles="OpenStreetMap")
        folium.GeoJson(
            gdf_wgs.__geo_interface__,
            name=title or src.stem,
        ).add_to(m)
        folium.LayerControl().add_to(m)
        m.save(str(out))
    elif _is_raster(src):
        # For raster HTML, create a simple bounds overlay
        rasterio = require_extra("rasterio", "geo")
        with rasterio.open(src) as ds:
            from pyproj import Transformer

            if ds.crs and not ds.crs.is_geographic:
                transformer = Transformer.from_crs(ds.crs, "EPSG:4326", always_xy=True)
                left, bottom = transformer.transform(ds.bounds.left, ds.bounds.bottom)
                right, top = transformer.transform(ds.bounds.right, ds.bounds.top)
            else:
                left, bottom, right, top = ds.bounds

            center = [(bottom + top) / 2, (left + right) / 2]
            m = folium.Map(location=center, zoom_start=8)
            folium.Rectangle(
                bounds=[[bottom, left], [top, right]],
                color="red",
                tooltip=title or src.stem,
            ).add_to(m)
            m.save(str(out))
    else:
        raise FileFormatError(
            f"Cannot determine type of '{src.name}'",
            hint="Use a recognized vector or raster extension.",
        )

    logger.info("Interactive map saved to %s", out)
    return out
