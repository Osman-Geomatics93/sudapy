"""Tests for CRS registry and suggestion logic."""

from __future__ import annotations

import pytest

from sudapy.crs.registry import (
    get_preset,
    list_presets,
    suggest_utm_zone,
    validate_epsg,
)


class TestListPresets:
    def test_returns_nonempty_list(self):
        presets = list_presets()
        assert len(presets) >= 6

    def test_contains_wgs84(self):
        presets = list_presets()
        epsg_codes = [p.epsg for p in presets]
        assert 4326 in epsg_codes

    def test_contains_adindan(self):
        presets = list_presets()
        epsg_codes = [p.epsg for p in presets]
        assert 20135 in epsg_codes
        assert 20136 in epsg_codes
        assert 20137 in epsg_codes

    def test_contains_zone_37(self):
        presets = list_presets()
        epsg_codes = [p.epsg for p in presets]
        assert 32637 in epsg_codes
        assert 20137 in epsg_codes


class TestGetPreset:
    def test_existing(self):
        p = get_preset(32635)
        assert p is not None
        assert p.name == "WGS 84 / UTM zone 35N"

    def test_missing(self):
        assert get_preset(99999) is None


class TestSuggestUTMZone:
    def test_khartoum(self):
        # Khartoum is roughly at lon=32.5, lat=15.6 -> UTM zone 36N
        suggestions = suggest_utm_zone(32.5, 15.6)
        assert len(suggestions) >= 1
        epsg_codes = [s["epsg"] for s in suggestions]
        assert 32636 in epsg_codes

    def test_khartoum_adindan_suggested(self):
        suggestions = suggest_utm_zone(32.5, 15.6)
        epsg_codes = [s["epsg"] for s in suggestions]
        # Zone 36 has Adindan preset
        assert 20136 in epsg_codes

    def test_western_sudan(self):
        # El Fasher: roughly lon=25.3, lat=13.6 -> UTM zone 35N
        suggestions = suggest_utm_zone(25.3, 13.6)
        epsg_codes = [s["epsg"] for s in suggestions]
        assert 32635 in epsg_codes

    def test_red_sea_coast(self):
        # Port Sudan: roughly lon=37.2, lat=19.6 -> UTM zone 37N
        suggestions = suggest_utm_zone(37.2, 19.6)
        epsg_codes = [s["epsg"] for s in suggestions]
        assert 32637 in epsg_codes
        assert 20137 in epsg_codes

    def test_southern_hemisphere(self):
        suggestions = suggest_utm_zone(32.5, -5.0)
        assert suggestions[0]["hemisphere"] == "S"
        assert suggestions[0]["epsg"] == 32736  # zone 36S

    def test_invalid_longitude(self):
        with pytest.raises(ValueError, match="Longitude"):
            suggest_utm_zone(200, 15)

    def test_invalid_latitude(self):
        with pytest.raises(ValueError, match="Latitude"):
            suggest_utm_zone(32, 100)


class TestValidateEpsg:
    def test_valid(self):
        crs = validate_epsg(4326)
        assert crs.to_epsg() == 4326

    def test_invalid(self):
        from sudapy.core.errors import CRSError

        with pytest.raises(CRSError):
            validate_epsg(0)
