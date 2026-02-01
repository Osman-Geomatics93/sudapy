"""Built-in CRS registry for Sudan and surrounding regions.

Contains common coordinate reference systems used in Sudanese geomatics,
plus a helper to suggest the appropriate UTM zone for a given coordinate.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from pyproj import CRS


@dataclass(frozen=True)
class CRSPreset:
    """A named CRS preset."""

    epsg: int
    name: str
    description: str
    region: str


# ---------------------------------------------------------------------------
# Built-in presets
# ---------------------------------------------------------------------------

SUDAN_CRS_PRESETS: list[CRSPreset] = [
    CRSPreset(
        epsg=4326,
        name="WGS 84",
        description="Global geographic CRS (latitude / longitude)",
        region="Global",
    ),
    CRSPreset(
        epsg=32634,
        name="WGS 84 / UTM zone 34N",
        description="UTM zone covering western Sudan (~18-24 E)",
        region="Western Sudan",
    ),
    CRSPreset(
        epsg=32635,
        name="WGS 84 / UTM zone 35N",
        description="UTM zone covering central Sudan (~24-30 E)",
        region="Central Sudan",
    ),
    CRSPreset(
        epsg=32636,
        name="WGS 84 / UTM zone 36N",
        description="UTM zone covering eastern Sudan (~30-36 E)",
        region="Eastern Sudan",
    ),
    CRSPreset(
        epsg=32637,
        name="WGS 84 / UTM zone 37N",
        description="UTM zone covering far-eastern Sudan and Red Sea coast (~36-42 E)",
        region="Red Sea / Far-Eastern Sudan",
    ),
    CRSPreset(
        epsg=20135,
        name="Adindan / UTM zone 35N",
        description="Legacy Adindan datum, UTM zone 35N",
        region="Central Sudan (legacy surveys)",
    ),
    CRSPreset(
        epsg=20136,
        name="Adindan / UTM zone 36N",
        description="Legacy Adindan datum, UTM zone 36N",
        region="Eastern Sudan (legacy surveys)",
    ),
    CRSPreset(
        epsg=20137,
        name="Adindan / UTM zone 37N",
        description="Legacy Adindan datum, UTM zone 37N",
        region="Red Sea / Far-Eastern Sudan (legacy surveys)",
    ),
]


def list_presets() -> list[CRSPreset]:
    """Return all built-in Sudan CRS presets."""
    return list(SUDAN_CRS_PRESETS)


def get_preset(epsg: int) -> CRSPreset | None:
    """Lookup a preset by EPSG code. Returns ``None`` if not found."""
    for p in SUDAN_CRS_PRESETS:
        if p.epsg == epsg:
            return p
    return None


def suggest_utm_zone(lon: float, lat: float) -> list[dict]:
    """Suggest appropriate UTM EPSG codes for a given longitude/latitude.

    Args:
        lon: Longitude in decimal degrees.
        lat: Latitude in decimal degrees.

    Returns:
        A list of dicts with keys ``epsg``, ``zone``, ``hemisphere``, ``name``.
    """
    if not (-180 <= lon <= 180):
        raise ValueError(f"Longitude {lon} out of range [-180, 180]")
    if not (-90 <= lat <= 90):
        raise ValueError(f"Latitude {lat} out of range [-90, 90]")

    zone_number = int(math.floor((lon + 180) / 6)) + 1
    hemisphere = "N" if lat >= 0 else "S"

    base_epsg = 32600 if hemisphere == "N" else 32700
    wgs84_epsg = base_epsg + zone_number

    suggestions: list[dict] = [
        {
            "epsg": wgs84_epsg,
            "zone": zone_number,
            "hemisphere": hemisphere,
            "name": f"WGS 84 / UTM zone {zone_number}{hemisphere}",
            "datum": "WGS 84",
        },
    ]

    # If the point falls in a zone covered by Adindan presets, suggest those too.
    adindan_map = {35: 20135, 36: 20136, 37: 20137}
    if zone_number in adindan_map and hemisphere == "N":
        suggestions.append(
            {
                "epsg": adindan_map[zone_number],
                "zone": zone_number,
                "hemisphere": hemisphere,
                "name": f"Adindan / UTM zone {zone_number}N",
                "datum": "Adindan",
            }
        )

    return suggestions


def validate_epsg(epsg: int) -> CRS:
    """Return a :class:`pyproj.CRS` for the given EPSG code or raise.

    Args:
        epsg: EPSG code.

    Returns:
        A ``pyproj.CRS`` instance.

    Raises:
        sudapy.core.errors.CRSError: If the EPSG code is invalid.
    """
    from sudapy.core.errors import CRSError

    try:
        return CRS.from_epsg(epsg)
    except Exception as exc:
        raise CRSError(
            f"Invalid EPSG code: {epsg}",
            hint="Use 'sudapy crs list' to see common Sudan CRS presets.",
        ) from exc
