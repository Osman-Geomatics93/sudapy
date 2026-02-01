"""Sentinel satellite scene search and download via sentinelsat.

Requires the ``sudapy[rs]`` extra:  ``pip install "sudapy[rs]"``

Before first use, set your Copernicus Open Access Hub credentials:

    export COPERNICUS_USER=your_username
    export COPERNICUS_PASSWORD=your_password

Register at https://scihub.copernicus.eu/dhus/#/self-registration
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Union

from sudapy.core.errors import DependencyError, SudaPyError
from sudapy.core.logging import get_logger

logger = get_logger(__name__)

PathLike = Union[str, Path]

_HUB_URL = "https://apihub.copernicus.eu/apihub"


def _get_api():
    """Return a configured SentinelAPI instance."""
    try:
        from sentinelsat import SentinelAPI
    except ImportError as exc:
        raise DependencyError(
            "sentinelsat is required for Sentinel operations.",
            hint='pip install "sudapy[rs]"',
        ) from exc

    user = os.environ.get("COPERNICUS_USER", "")
    password = os.environ.get("COPERNICUS_PASSWORD", "")

    if not user or not password:
        raise SudaPyError(
            "Copernicus credentials not set.",
            hint=(
                "Set environment variables COPERNICUS_USER and COPERNICUS_PASSWORD.\n"
                "  Register at: https://scihub.copernicus.eu/dhus/#/self-registration"
            ),
        )

    return SentinelAPI(user, password, _HUB_URL)


def search_scenes(
    *,
    lon: float,
    lat: float,
    start_date: str,
    end_date: str,
    platform_name: str = "Sentinel-2",
    max_cloud: int = 30,
) -> list[dict]:
    """Search for Sentinel scenes around a point.

    Args:
        lon: Center longitude.
        lat: Center latitude.
        start_date: Start date as YYYY-MM-DD.
        end_date: End date as YYYY-MM-DD.
        platform_name: Satellite platform (default ``Sentinel-2``).
        max_cloud: Maximum cloud cover percentage (default 30).

    Returns:
        List of dicts with keys: ``uuid``, ``title``, ``date``, ``cloud_cover``.
    """
    api = _get_api()

    # Create a small point footprint
    footprint = f"POINT({lon} {lat})"

    products = api.query(
        footprint,
        date=(start_date.replace("-", ""), end_date.replace("-", "")),
        platformname=platform_name,
        cloudcoverpercentage=(0, max_cloud),
    )

    results = []
    for uid, meta in products.items():
        results.append({
            "uuid": uid,
            "title": meta.get("title", ""),
            "date": str(meta.get("beginposition", ""))[:10],
            "cloud_cover": meta.get("cloudcoverpercentage", -1),
        })

    # Sort by date descending
    results.sort(key=lambda r: r["date"], reverse=True)
    logger.info("Found %d scenes", len(results))
    return results


def download_scene(
    *,
    uuid: str,
    out_dir: PathLike = ".",
) -> Path:
    """Download a Sentinel scene by UUID.

    Args:
        uuid: Scene UUID from :func:`search_scenes`.
        out_dir: Output directory (default: current directory).

    Returns:
        Path to the downloaded file.
    """
    api = _get_api()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Downloading scene %s to %s ...", uuid, out_dir)
    result = api.download(uuid, directory_path=str(out_dir))

    downloaded_path = Path(result["path"])
    logger.info("Download complete: %s", downloaded_path)
    return downloaded_path
