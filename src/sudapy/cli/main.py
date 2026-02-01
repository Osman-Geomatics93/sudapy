"""SudaPy command-line interface.

Built with Typer for clean help text and autocompletion support.
"""

from __future__ import annotations

import os
import platform
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

import sudapy

console = Console()

# ---------------------------------------------------------------------------
# Root app
# ---------------------------------------------------------------------------

app = typer.Typer(
    name="sudapy",
    help="SudaPy: Sudan-focused Python toolkit for Geomatics.",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)

# ---------------------------------------------------------------------------
# Sub-command groups
# ---------------------------------------------------------------------------

crs_app = typer.Typer(help="Coordinate Reference System utilities.")
vector_app = typer.Typer(help="Vector geoprocessing operations.")
raster_app = typer.Typer(help="Raster geoprocessing operations.")
map_app = typer.Typer(help="Quick map visualization.")
rs_app = typer.Typer(help="Remote sensing tools (requires sudapy[rs]).")

app.add_typer(crs_app, name="crs")
app.add_typer(vector_app, name="vector")
app.add_typer(raster_app, name="raster")
app.add_typer(map_app, name="map")
app.add_typer(rs_app, name="rs")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _handle_error(exc: Exception) -> None:
    """Print a rich-formatted error and exit."""
    from sudapy.core.errors import DependencyError

    console.print(f"[bold red]Error:[/bold red] {exc}")
    if isinstance(exc, DependencyError) and exc.hint:
        console.print(f"[yellow]Install the missing extra:[/yellow] {exc.hint}")
    raise typer.Exit(code=1)


def _check_module(name: str) -> tuple[str, str]:
    """Return (version, status_style) for a module."""
    try:
        mod = __import__(name)
        ver = getattr(mod, "__version__", "installed")
        return ver, "green"
    except ImportError:
        return "not installed", "red"


# ---------------------------------------------------------------------------
# sudapy info
# ---------------------------------------------------------------------------

@app.command()
def info() -> None:
    """Show SudaPy version, environment, and key dependency info."""
    table = Table(title="SudaPy Environment", show_lines=True)
    table.add_column("Component", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("SudaPy version", sudapy.__version__)
    table.add_row("Python", sys.version.split()[0])
    table.add_row("Platform", platform.platform())

    for mod_name in ("geopandas", "shapely", "fiona", "pyproj", "rasterio", "numpy", "pandas"):
        ver, style = _check_module(mod_name)
        table.add_row(mod_name, f"[{style}]{ver}[/{style}]")

    try:
        import rasterio
        table.add_row("GDAL (via rasterio)", rasterio.gdal_version())
    except Exception:
        table.add_row("GDAL", "[red]unavailable[/red]")

    console.print(table)


# ---------------------------------------------------------------------------
# sudapy doctor
# ---------------------------------------------------------------------------

@app.command()
def doctor() -> None:
    """Run diagnostics to check if SudaPy's environment is healthy."""
    # status can be: True (PASS), False (FAIL), or None (SKIP/optional missing)
    checks: list[tuple[str, bool | None, str]] = []

    # Python version
    py_ver = sys.version_info
    ok = py_ver >= (3, 9)
    checks.append((
        "Python >= 3.9",
        ok,
        f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}" + ("" if ok else " -- upgrade to 3.9+"),
    ))

    # Core imports (always required)
    for mod, label in [
        ("pyproj", "pyproj import"),
        ("pandas", "pandas import"),
    ]:
        try:
            __import__(mod)
            checks.append((label, True, "OK"))
        except ImportError:
            checks.append((label, False, "not installed -- pip install sudapy"))

    # PROJ data
    try:
        from pyproj import CRS
        crs = CRS.from_epsg(32636)
        checks.append(("PROJ data available", True, f"OK ({crs.name})"))
    except Exception as exc:
        checks.append(("PROJ data available", False, str(exc)))

    # Optional geo imports (sudapy[geo])
    for mod, label in [
        ("geopandas", "geopandas import (optional)"),
        ("shapely", "shapely import (optional)"),
        ("fiona", "fiona import (optional)"),
        ("numpy", "numpy import (optional)"),
    ]:
        try:
            __import__(mod)
            checks.append((label, True, "OK"))
        except ImportError:
            checks.append((label, None, 'not installed -- pip install "sudapy[geo]"'))

    # rasterio + GDAL (optional)
    try:
        import rasterio
        checks.append(("rasterio import (optional)", True, f"OK (GDAL {rasterio.gdal_version()})"))
    except ImportError:
        checks.append((
            "rasterio import (optional)",
            None,
            'not installed -- pip install "sudapy[geo]"',
        ))

    # GeoPackage read/write (only if geo deps available)
    try:
        import geopandas as gpd
        from shapely.geometry import Point
        import tempfile

        gdf = gpd.GeoDataFrame({"val": [1]}, geometry=[Point(0, 0)], crs="EPSG:4326")
        with tempfile.NamedTemporaryFile(suffix=".gpkg", delete=False) as tmp:
            tmp_path = tmp.name
        gdf.to_file(tmp_path, driver="GPKG")
        gpd.read_file(tmp_path)
        os.unlink(tmp_path)
        checks.append(("GeoPackage read/write", True, "OK"))
    except ImportError:
        checks.append(("GeoPackage read/write", None, 'skipped -- install "sudapy[geo]" first'))
    except Exception as exc:
        checks.append(("GeoPackage read/write", False, str(exc)))

    # Print results
    table = Table(title="SudaPy Doctor", show_lines=True)
    table.add_column("Check", style="cyan")
    table.add_column("Status")
    table.add_column("Details")

    has_fail = False
    for label, ok, detail in checks:
        if ok is True:
            status = "[green]PASS[/green]"
        elif ok is None:
            status = "[yellow]SKIP[/yellow]"
        else:
            status = "[red]FAIL[/red]"
            has_fail = True
        table.add_row(label, status, detail)

    console.print(table)

    if has_fail:
        console.print(
            "\n[bold red]Some core checks failed.[/bold red] See hints above."
        )
    else:
        console.print(
            "\n[bold green]Core checks passed.[/bold green] "
            'Install geo extras for vector/raster support: pip install "sudapy[geo]"'
        )


# ---------------------------------------------------------------------------
# sudapy init
# ---------------------------------------------------------------------------

@app.command()
def init(
    name: str = typer.Argument(..., help="Project folder name to create."),
) -> None:
    """Scaffold a standard geomatics project folder structure."""
    root = Path(name)
    if root.exists():
        console.print(f"[bold red]Error:[/bold red] Directory '{name}' already exists.")
        raise typer.Exit(code=1)

    folders = [
        root / "data_raw",
        root / "data_clean",
        root / "outputs",
        root / "maps",
        root / "scripts",
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

    # Create a minimal README
    (root / "README.md").write_text(
        f"# {name}\n\n"
        f"Geomatics project created with [SudaPy](https://pypi.org/project/sudapy/).\n\n"
        f"## Folder structure\n\n"
        f"- `data_raw/` -- original source data (do not modify)\n"
        f"- `data_clean/` -- cleaned / processed data\n"
        f"- `outputs/` -- analysis results, tables, statistics\n"
        f"- `maps/` -- exported maps (PNG, HTML)\n"
        f"- `scripts/` -- processing scripts\n",
        encoding="utf-8",
    )

    # Create a placeholder script
    (root / "scripts" / "process.py").write_text(
        '"""Processing script -- edit this for your workflow."""\n\n'
        "from sudapy.crs.registry import suggest_utm_zone\n"
        "from sudapy.vector.ops import reproject\n\n"
        "# Example: suggest CRS for Khartoum\n"
        "print(suggest_utm_zone(lon=32.5, lat=15.6))\n",
        encoding="utf-8",
    )

    console.print(f"[green]Project '{name}' created with folders:[/green]")
    for folder in folders:
        console.print(f"  {folder}/")


# ---------------------------------------------------------------------------
# sudapy report
# ---------------------------------------------------------------------------

@app.command()
def report(
    input_path: Path = typer.Option(..., "--in", help="Input vector file."),
) -> None:
    """Print a summary report for a vector dataset."""
    try:
        import geopandas as gpd
    except ImportError:
        _handle_error(Exception('geopandas is required. Install with: pip install "sudapy[geo]"'))
        return

    try:
        gdf = gpd.read_file(input_path)
    except Exception as exc:
        _handle_error(exc)
        return

    table = Table(title=f"Report: {input_path.name}", show_lines=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Features", str(len(gdf)))
    table.add_row("Columns", ", ".join(gdf.columns.tolist()))
    table.add_row("Geometry type", str(gdf.geometry.geom_type.unique().tolist()))
    table.add_row("CRS", str(gdf.crs) if gdf.crs else "[red]None[/red]")

    bounds = gdf.total_bounds
    table.add_row("Bounds (minx, miny, maxx, maxy)",
                  f"{bounds[0]:.6f}, {bounds[1]:.6f}, {bounds[2]:.6f}, {bounds[3]:.6f}")

    # Null geometries
    null_count = int(gdf.geometry.isna().sum())
    style = "red" if null_count > 0 else "green"
    table.add_row("Null geometries", f"[{style}]{null_count}[/{style}]")

    # Invalid geometries
    try:
        invalid_count = int((~gdf.geometry.is_valid).sum())
        style = "red" if invalid_count > 0 else "green"
        table.add_row("Invalid geometries", f"[{style}]{invalid_count}[/{style}]")
    except Exception:
        table.add_row("Invalid geometries", "[yellow]could not check[/yellow]")

    console.print(table)


# ---------------------------------------------------------------------------
# sudapy batch
# ---------------------------------------------------------------------------

@app.command()
def batch(
    operation: str = typer.Argument(
        ...,
        help="Operation to run: reproject, clip, buffer, area, simplify, fix-geometry.",
    ),
    input_dir: Path = typer.Option(..., "--in", help="Input directory with vector files."),
    output_dir: Path = typer.Option(..., "--out", help="Output directory."),
    to: Optional[int] = typer.Option(None, "--to", help="Target EPSG (for reproject)."),
    clip_path: Optional[Path] = typer.Option(None, "--clip", help="Clip geometry file."),
    distance: Optional[float] = typer.Option(None, "--distance", help="Buffer distance in meters."),
    field: str = typer.Option("area_m2", "--field", help="Field name (for area)."),
    tolerance: Optional[float] = typer.Option(None, "--tolerance", help="Simplify tolerance in meters."),
) -> None:
    """Run an operation on all vector files in a directory."""
    from sudapy.vector import ops as vops

    SUPPORTED_EXTS = {".gpkg", ".geojson", ".json", ".shp"}
    files = sorted(f for f in input_dir.iterdir() if f.suffix.lower() in SUPPORTED_EXTS)

    if not files:
        console.print(f"[yellow]No vector files found in {input_dir}[/yellow]")
        raise typer.Exit(code=1)

    output_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"Processing {len(files)} files with operation '{operation}' ...")

    ok_count = 0
    for f in files:
        out = output_dir / f.name
        try:
            if operation == "reproject":
                if to is None:
                    _handle_error(Exception("--to EPSG is required for reproject"))
                    return
                vops.reproject(f, to_epsg=to, out=out)
            elif operation == "clip":
                if clip_path is None:
                    _handle_error(Exception("--clip path is required for clip"))
                    return
                vops.clip(f, clip_path, out=out)
            elif operation == "buffer":
                if distance is None:
                    _handle_error(Exception("--distance is required for buffer"))
                    return
                vops.buffer(f, distance_m=distance, out=out)
            elif operation == "area":
                vops.calculate_area(f, field=field, out=out)
            elif operation == "simplify":
                if tolerance is None:
                    _handle_error(Exception("--tolerance is required for simplify"))
                    return
                vops.simplify(f, tolerance_m=tolerance, out=out)
            elif operation == "fix-geometry":
                vops.fix_geometry(f, out=out)
            else:
                _handle_error(Exception(
                    f"Unknown operation '{operation}'. "
                    "Supported: reproject, clip, buffer, area, simplify, fix-geometry"
                ))
                return
            ok_count += 1
            console.print(f"  [green]OK[/green] {f.name}")
        except Exception as exc:
            console.print(f"  [red]FAIL[/red] {f.name}: {exc}")

    console.print(f"\n[green]{ok_count}/{len(files)} files processed -> {output_dir}[/green]")


# ---------------------------------------------------------------------------
# sudapy crs list
# ---------------------------------------------------------------------------

@crs_app.command("list")
def crs_list() -> None:
    """Show common CRS presets used in Sudan."""
    from sudapy.crs.registry import list_presets

    table = Table(title="Sudan CRS Presets")
    table.add_column("EPSG", style="cyan", justify="right")
    table.add_column("Name", style="green")
    table.add_column("Region", style="yellow")
    table.add_column("Description")

    for p in list_presets():
        table.add_row(str(p.epsg), p.name, p.region, p.description)

    console.print(table)


# ---------------------------------------------------------------------------
# sudapy crs suggest
# ---------------------------------------------------------------------------

@crs_app.command("suggest")
def crs_suggest(
    lon: float = typer.Option(..., "--lon", help="Longitude in decimal degrees."),
    lat: float = typer.Option(..., "--lat", help="Latitude in decimal degrees."),
) -> None:
    """Suggest the most likely UTM zone / EPSG for a coordinate."""
    from sudapy.crs.registry import suggest_utm_zone

    try:
        suggestions = suggest_utm_zone(lon, lat)
    except ValueError as exc:
        _handle_error(exc)
        return

    table = Table(title=f"CRS Suggestions for ({lon}, {lat})")
    table.add_column("EPSG", style="cyan", justify="right")
    table.add_column("Name", style="green")
    table.add_column("Datum")

    for s in suggestions:
        table.add_row(str(s["epsg"]), s["name"], s["datum"])

    console.print(table)


# ---------------------------------------------------------------------------
# sudapy vector reproject
# ---------------------------------------------------------------------------

@vector_app.command("reproject")
def vector_reproject(
    input_path: Path = typer.Option(..., "--in", help="Input vector file."),
    output_path: Path = typer.Option(..., "--out", help="Output vector file."),
    to: int = typer.Option(..., "--to", help="Target EPSG code."),
) -> None:
    """Reproject a vector dataset to a new CRS."""
    from sudapy.vector.ops import reproject

    try:
        reproject(input_path, to_epsg=to, out=output_path)
        console.print(f"[green]Reprojected to EPSG:{to} -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy vector clip
# ---------------------------------------------------------------------------

@vector_app.command("clip")
def vector_clip(
    input_path: Path = typer.Option(..., "--in", help="Input vector file."),
    clip_path: Path = typer.Option(..., "--clip", help="Clipping geometry file."),
    output_path: Path = typer.Option(..., "--out", help="Output vector file."),
) -> None:
    """Clip a vector dataset by another geometry."""
    from sudapy.vector.ops import clip

    try:
        clip(input_path, clip_path, out=output_path)
        console.print(f"[green]Clipped -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy vector dissolve
# ---------------------------------------------------------------------------

@vector_app.command("dissolve")
def vector_dissolve(
    input_path: Path = typer.Option(..., "--in", help="Input vector file."),
    by: str = typer.Option(..., "--by", help="Field name to dissolve on."),
    output_path: Path = typer.Option(..., "--out", help="Output vector file."),
) -> None:
    """Dissolve geometries by an attribute field."""
    from sudapy.vector.ops import dissolve

    try:
        dissolve(input_path, by=by, out=output_path)
        console.print(f"[green]Dissolved by '{by}' -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy vector area
# ---------------------------------------------------------------------------

@vector_app.command("area")
def vector_area(
    input_path: Path = typer.Option(..., "--in", help="Input vector file."),
    field: str = typer.Option("area_m2", "--field", help="Name for the new area column."),
    output_path: Path = typer.Option(..., "--out", help="Output vector file."),
) -> None:
    """Calculate geometry area in square meters."""
    from sudapy.vector.ops import calculate_area

    try:
        calculate_area(input_path, field=field, out=output_path)
        console.print(f"[green]Area calculated (column '{field}') -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy vector buffer
# ---------------------------------------------------------------------------

@vector_app.command("buffer")
def vector_buffer(
    input_path: Path = typer.Option(..., "--in", help="Input vector file."),
    distance: float = typer.Option(..., "--distance", help="Buffer distance in meters."),
    output_path: Path = typer.Option(..., "--out", help="Output vector file."),
) -> None:
    """Buffer geometries by a distance in meters."""
    from sudapy.vector.ops import buffer

    try:
        buffer(input_path, distance_m=distance, out=output_path)
        console.print(f"[green]Buffered by {distance}m -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy vector simplify
# ---------------------------------------------------------------------------

@vector_app.command("simplify")
def vector_simplify(
    input_path: Path = typer.Option(..., "--in", help="Input vector file."),
    tolerance: float = typer.Option(..., "--tolerance", help="Simplification tolerance in meters."),
    output_path: Path = typer.Option(..., "--out", help="Output vector file."),
) -> None:
    """Simplify geometries to reduce vertex count."""
    from sudapy.vector.ops import simplify

    try:
        simplify(input_path, tolerance_m=tolerance, out=output_path)
        console.print(f"[green]Simplified (tolerance={tolerance}m) -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy vector fix-geometry
# ---------------------------------------------------------------------------

@vector_app.command("fix-geometry")
def vector_fix_geometry(
    input_path: Path = typer.Option(..., "--in", help="Input vector file."),
    output_path: Path = typer.Option(..., "--out", help="Output vector file."),
) -> None:
    """Repair invalid geometries using make_valid."""
    from sudapy.vector.ops import fix_geometry

    try:
        fix_geometry(input_path, out=output_path)
        console.print(f"[green]Geometries fixed -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy raster clip
# ---------------------------------------------------------------------------

@raster_app.command("clip")
def raster_clip(
    input_path: Path = typer.Option(..., "--in", help="Input raster file."),
    clip_path: Path = typer.Option(..., "--clip", help="Clipping vector file."),
    output_path: Path = typer.Option(..., "--out", help="Output raster file."),
) -> None:
    """Clip a raster by vector geometries."""
    from sudapy.raster.ops import clip

    try:
        clip(input_path, clip_path, out=output_path)
        console.print(f"[green]Raster clipped -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy raster reproject
# ---------------------------------------------------------------------------

@raster_app.command("reproject")
def raster_reproject(
    input_path: Path = typer.Option(..., "--in", help="Input raster file."),
    output_path: Path = typer.Option(..., "--out", help="Output raster file."),
    to: int = typer.Option(..., "--to", help="Target EPSG code."),
) -> None:
    """Reproject a raster to a new CRS."""
    from sudapy.raster.ops import reproject_raster

    try:
        reproject_raster(input_path, output_path, to_epsg=to)
        console.print(f"[green]Raster reprojected to EPSG:{to} -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy raster resample
# ---------------------------------------------------------------------------

@raster_app.command("resample")
def raster_resample(
    input_path: Path = typer.Option(..., "--in", help="Input raster file."),
    output_path: Path = typer.Option(..., "--out", help="Output raster file."),
    scale: float = typer.Option(..., "--scale", help="Scale factor (2.0 = double resolution)."),
    method: str = typer.Option("bilinear", "--method", help="Resampling: nearest, bilinear, cubic."),
) -> None:
    """Resample a raster to a different resolution."""
    from sudapy.raster.ops import resample

    try:
        resample(input_path, output_path, scale_factor=scale, method=method)
        console.print(f"[green]Resampled (x{scale}, {method}) -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy raster mosaic
# ---------------------------------------------------------------------------

@raster_app.command("mosaic")
def raster_mosaic(
    input_dir: Path = typer.Option(..., "--in", help="Directory with raster tiles."),
    output_path: Path = typer.Option(..., "--out", help="Output merged raster file."),
) -> None:
    """Merge multiple raster tiles into one."""
    from sudapy.raster.ops import mosaic

    try:
        mosaic(input_dir, output_path)
        console.print(f"[green]Mosaic created -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy raster hillshade
# ---------------------------------------------------------------------------

@raster_app.command("hillshade")
def raster_hillshade(
    input_path: Path = typer.Option(..., "--in", help="Input DEM raster."),
    output_path: Path = typer.Option(..., "--out", help="Output hillshade raster."),
    azimuth: float = typer.Option(315.0, "--azimuth", help="Sun azimuth in degrees."),
    altitude: float = typer.Option(45.0, "--altitude", help="Sun altitude in degrees."),
) -> None:
    """Generate a hillshade from a DEM."""
    from sudapy.raster.ops import hillshade

    try:
        hillshade(input_path, output_path, azimuth=azimuth, altitude=altitude)
        console.print(f"[green]Hillshade -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy raster slope
# ---------------------------------------------------------------------------

@raster_app.command("slope")
def raster_slope(
    input_path: Path = typer.Option(..., "--in", help="Input DEM raster."),
    output_path: Path = typer.Option(..., "--out", help="Output slope raster (degrees)."),
) -> None:
    """Calculate slope in degrees from a DEM."""
    from sudapy.raster.ops import slope

    try:
        slope(input_path, output_path)
        console.print(f"[green]Slope -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy map quick
# ---------------------------------------------------------------------------

@map_app.command("quick")
def map_quick(
    input_path: Path = typer.Option(..., "--in", help="Input vector or raster file."),
    output_path: Path = typer.Option(..., "--out", help="Output .png or .html file."),
) -> None:
    """Generate a quick visualization of a dataset."""
    from sudapy.viz.maps import quick_map

    try:
        quick_map(input_path, output_path)
        console.print(f"[green]Map exported -> {output_path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy rs sentinel-search
# ---------------------------------------------------------------------------

@rs_app.command("sentinel-search")
def rs_sentinel_search(
    lon: float = typer.Option(..., "--lon", help="Center longitude."),
    lat: float = typer.Option(..., "--lat", help="Center latitude."),
    start: str = typer.Option(..., "--start", help="Start date (YYYY-MM-DD)."),
    end: str = typer.Option(..., "--end", help="End date (YYYY-MM-DD)."),
    platform_name: str = typer.Option("Sentinel-2", "--platform", help="Satellite platform."),
    max_cloud: int = typer.Option(30, "--max-cloud", help="Max cloud cover percentage."),
) -> None:
    """Search for Sentinel satellite scenes (requires sudapy[rs])."""
    from sudapy.rs.sentinel import search_scenes

    try:
        results = search_scenes(
            lon=lon, lat=lat, start_date=start, end_date=end,
            platform_name=platform_name, max_cloud=max_cloud,
        )
        if not results:
            console.print("[yellow]No scenes found for the given parameters.[/yellow]")
            return

        table = Table(title=f"Sentinel Scenes ({len(results)} found)")
        table.add_column("UUID", style="cyan", max_width=12)
        table.add_column("Date", style="green")
        table.add_column("Cloud %")
        table.add_column("Title")

        for r in results[:20]:  # Show top 20
            table.add_row(
                r["uuid"][:12] + "...",
                r["date"],
                f"{r['cloud_cover']:.1f}",
                r["title"],
            )
        console.print(table)
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# sudapy rs sentinel-download
# ---------------------------------------------------------------------------

@rs_app.command("sentinel-download")
def rs_sentinel_download(
    uuid: str = typer.Option(..., "--uuid", help="Scene UUID from sentinel-search."),
    out_dir: Path = typer.Option(".", "--out", help="Output directory."),
) -> None:
    """Download a Sentinel scene by UUID (requires sudapy[rs])."""
    from sudapy.rs.sentinel import download_scene

    try:
        path = download_scene(uuid=uuid, out_dir=out_dir)
        console.print(f"[green]Downloaded -> {path}[/green]")
    except Exception as exc:
        _handle_error(exc)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
