# CLI Reference

SudaPy provides a command-line interface built with [Typer](https://typer.tiangolo.com/). All commands use `--in` / `--out` for input/output files.

```bash
sudapy --help
```

## Global commands

### `sudapy info`

Show SudaPy version, Python version, platform, and dependency status.

```bash
sudapy info
```

### `sudapy doctor`

Run environment diagnostics: checks Python version, core imports, GDAL, PROJ data, and GeoPackage read/write.

```bash
sudapy doctor
```

### `sudapy init`

Scaffold a new geomatics project with standard folder structure.

```bash
sudapy init PROJECT_NAME
```

Creates: `data_raw/`, `data_clean/`, `outputs/`, `maps/`, `scripts/process.py`, and `README.md`.

### `sudapy report`

Print a summary report for a vector dataset.

```bash
sudapy report --in data/parcels.gpkg
```

Reports: feature count, columns, geometry types, CRS, bounds, null/invalid geometry count.

### `sudapy batch`

Run an operation on all vector files in a directory.

```bash
sudapy batch OPERATION --in INPUT_DIR --out OUTPUT_DIR [OPTIONS]
```

Operations: `reproject`, `clip`, `buffer`, `area`, `simplify`, `fix-geometry`.

See [Batch Processing Guide](guide/batch.md) for details.

---

## CRS commands

### `sudapy crs list`

Show all built-in Sudan CRS presets.

```bash
sudapy crs list
```

### `sudapy crs suggest`

Suggest the appropriate UTM zone for a coordinate.

```bash
sudapy crs suggest --lon 32.5 --lat 15.6
```

| Option | Required | Description |
|--------|----------|-------------|
| `--lon` | Yes | Longitude in decimal degrees |
| `--lat` | Yes | Latitude in decimal degrees |

---

## Vector commands

### `sudapy vector reproject`

```bash
sudapy vector reproject --in INPUT --out OUTPUT --to EPSG
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input vector file |
| `--out` | Yes | Output vector file |
| `--to` | Yes | Target EPSG code |

### `sudapy vector clip`

```bash
sudapy vector clip --in INPUT --clip MASK --out OUTPUT
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input vector file |
| `--clip` | Yes | Clipping geometry file |
| `--out` | Yes | Output vector file |

### `sudapy vector dissolve`

```bash
sudapy vector dissolve --in INPUT --by FIELD --out OUTPUT
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input vector file |
| `--by` | Yes | Field name to dissolve on |
| `--out` | Yes | Output vector file |

### `sudapy vector area`

```bash
sudapy vector area --in INPUT --out OUTPUT [--field FIELD]
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--in` | Yes | | Input vector file |
| `--out` | Yes | | Output vector file |
| `--field` | No | `area_m2` | Name for the area column |

### `sudapy vector buffer`

```bash
sudapy vector buffer --in INPUT --distance METERS --out OUTPUT
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input vector file |
| `--distance` | Yes | Buffer distance in meters |
| `--out` | Yes | Output vector file |

### `sudapy vector simplify`

```bash
sudapy vector simplify --in INPUT --tolerance METERS --out OUTPUT
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input vector file |
| `--tolerance` | Yes | Simplification tolerance in meters |
| `--out` | Yes | Output vector file |

### `sudapy vector fix-geometry`

```bash
sudapy vector fix-geometry --in INPUT --out OUTPUT
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input vector file |
| `--out` | Yes | Output vector file |

---

## Raster commands

### `sudapy raster clip`

```bash
sudapy raster clip --in INPUT --clip VECTOR --out OUTPUT
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input raster file |
| `--clip` | Yes | Clipping vector file |
| `--out` | Yes | Output raster file |

### `sudapy raster reproject`

```bash
sudapy raster reproject --in INPUT --out OUTPUT --to EPSG
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input raster file |
| `--out` | Yes | Output raster file |
| `--to` | Yes | Target EPSG code |

### `sudapy raster resample`

```bash
sudapy raster resample --in INPUT --out OUTPUT --scale FACTOR [--method METHOD]
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--in` | Yes | | Input raster file |
| `--out` | Yes | | Output raster file |
| `--scale` | Yes | | Scale factor (2.0 = double resolution) |
| `--method` | No | `bilinear` | Resampling: `nearest`, `bilinear`, `cubic` |

### `sudapy raster mosaic`

```bash
sudapy raster mosaic --in TILE_DIR --out OUTPUT
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Directory with raster tiles |
| `--out` | Yes | Output merged raster |

### `sudapy raster hillshade`

```bash
sudapy raster hillshade --in DEM --out OUTPUT [--azimuth DEG] [--altitude DEG]
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--in` | Yes | | Input DEM raster |
| `--out` | Yes | | Output hillshade raster |
| `--azimuth` | No | `315.0` | Sun azimuth in degrees |
| `--altitude` | No | `45.0` | Sun altitude in degrees |

### `sudapy raster slope`

```bash
sudapy raster slope --in DEM --out OUTPUT
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input DEM raster |
| `--out` | Yes | Output slope raster (degrees) |

---

## Map commands

### `sudapy map quick`

```bash
sudapy map quick --in INPUT --out OUTPUT
```

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input vector or raster file |
| `--out` | Yes | Output `.png` (static) or `.html` (interactive) |

---

## Remote sensing commands

!!! note
    Requires `pip install "sudapy[rs]"` and Copernicus credentials.

### `sudapy rs sentinel-search`

```bash
sudapy rs sentinel-search --lon LON --lat LAT --start DATE --end DATE [--platform NAME] [--max-cloud PCT]
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--lon` | Yes | | Center longitude |
| `--lat` | Yes | | Center latitude |
| `--start` | Yes | | Start date (YYYY-MM-DD) |
| `--end` | Yes | | End date (YYYY-MM-DD) |
| `--platform` | No | `Sentinel-2` | Satellite platform |
| `--max-cloud` | No | `30` | Max cloud cover % |

### `sudapy rs sentinel-download`

```bash
sudapy rs sentinel-download --uuid UUID [--out DIR]
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--uuid` | Yes | | Scene UUID from search |
| `--out` | No | `.` | Output directory |
