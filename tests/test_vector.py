"""Tests for vector operations."""

from __future__ import annotations

import warnings

import geopandas as gpd
import pytest
from shapely.geometry import Point, Polygon, box

from sudapy.vector.ops import (
    buffer,
    calculate_area,
    fix_geometry,
    reproject,
    simplify,
)


def _make_gdf(epsg: int = 32635) -> gpd.GeoDataFrame:
    """Create a tiny GeoDataFrame with a 1km x 1km box near Khartoum."""
    # In UTM 35N meters, a box near Khartoum
    geom = box(500_000, 1_700_000, 501_000, 1_701_000)
    return gpd.GeoDataFrame({"name": ["test"]}, geometry=[geom], crs=f"EPSG:{epsg}")


class TestReproject:
    def test_reproject_changes_crs(self):
        gdf = _make_gdf(32635)
        result = reproject(gdf, to_epsg=4326)
        assert result.crs.to_epsg() == 4326

    def test_reproject_preserves_rows(self):
        gdf = _make_gdf(32635)
        result = reproject(gdf, to_epsg=32636)
        assert len(result) == len(gdf)


class TestCalculateArea:
    def test_area_projected_crs(self):
        gdf = _make_gdf(32635)
        result = calculate_area(gdf, field="area_m2")
        assert "area_m2" in result.columns
        # 1km x 1km = 1,000,000 m^2
        area = result["area_m2"].iloc[0]
        assert abs(area - 1_000_000) < 1.0  # within 1 m^2

    def test_area_geographic_crs_warns(self):
        gdf = _make_gdf(32635).to_crs(4326)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = calculate_area(gdf, field="area_m2")
            assert len(w) == 1
            assert "geographic" in str(w[0].message).lower()
        assert "area_m2" in result.columns
        # Should still give a reasonable area (within 10% of 1km^2)
        area = result["area_m2"].iloc[0]
        assert 900_000 < area < 1_100_000

    def test_area_no_crs_raises(self):
        from sudapy.core.errors import CRSError

        gdf = _make_gdf(32635)
        gdf.crs = None
        with pytest.raises(CRSError):
            calculate_area(gdf)


class TestBuffer:
    def test_buffer_projected(self):
        gdf = _make_gdf(32635)
        result = buffer(gdf, distance_m=100)
        # Buffered area should be larger than original
        assert result.geometry.area.iloc[0] > gdf.geometry.area.iloc[0]

    def test_buffer_geographic_warns(self):
        gdf = _make_gdf(32635).to_crs(4326)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = buffer(gdf, distance_m=100)
            assert len(w) == 1
            assert "geographic" in str(w[0].message).lower()
        # Result should still be in WGS84
        assert result.crs.to_epsg() == 4326

    def test_buffer_no_crs_raises(self):
        from sudapy.core.errors import CRSError

        gdf = _make_gdf(32635)
        gdf.crs = None
        with pytest.raises(CRSError):
            buffer(gdf, distance_m=100)


class TestSimplify:
    def test_simplify_reduces_vertices(self):
        # Create a polygon with many vertices
        import numpy as np

        angles = np.linspace(0, 2 * np.pi, 100)
        coords = [(500_000 + 500 * np.cos(a), 1_700_000 + 500 * np.sin(a)) for a in angles]
        geom = Polygon(coords)
        gdf = gpd.GeoDataFrame({"name": ["circle"]}, geometry=[geom], crs="EPSG:32635")

        result = simplify(gdf, tolerance_m=50)
        # Simplified polygon should have fewer vertices
        original_coords = len(gdf.geometry.iloc[0].exterior.coords)
        simplified_coords = len(result.geometry.iloc[0].exterior.coords)
        assert simplified_coords < original_coords


class TestFixGeometry:
    def test_fixes_bowtie(self):
        # A self-intersecting "bowtie" polygon
        bowtie = Polygon([(0, 0), (1, 1), (1, 0), (0, 1), (0, 0)])
        gdf = gpd.GeoDataFrame({"name": ["bad"]}, geometry=[bowtie], crs="EPSG:32635")
        assert not gdf.geometry.is_valid.all()

        result = fix_geometry(gdf)
        assert result.geometry.is_valid.all()

    def test_valid_geometry_unchanged(self):
        gdf = _make_gdf(32635)
        assert gdf.geometry.is_valid.all()
        result = fix_geometry(gdf)
        assert result.geometry.is_valid.all()
        assert len(result) == len(gdf)
