# Batch Processing

The `sudapy batch` command applies a single operation to all vector files in a directory.

## Supported operations

| Operation | Required options | Description |
|-----------|-----------------|-------------|
| `reproject` | `--to EPSG` | Reproject all files |
| `clip` | `--clip FILE` | Clip all files by a geometry |
| `buffer` | `--distance METERS` | Buffer all geometries |
| `area` | `--field NAME` (optional) | Add area column |
| `simplify` | `--tolerance METERS` | Simplify geometries |
| `fix-geometry` | (none) | Repair invalid geometries |

## Usage

```bash
sudapy batch OPERATION --in INPUT_DIR --out OUTPUT_DIR [OPTIONS]
```

## Examples

### Reproject all files to UTM zone 36N

```bash
sudapy batch reproject --in data_raw/ --out data_clean/ --to 32636
```

### Buffer all files by 500 meters

```bash
sudapy batch buffer --in data_clean/ --out buffered/ --distance 500
```

### Calculate area for all files

```bash
sudapy batch area --in data_clean/ --out with_area/ --field area_m2
```

### Fix geometries in all files

```bash
sudapy batch fix-geometry --in problematic/ --out fixed/
```

### Clip all files by a boundary

```bash
sudapy batch clip --in state_data/ --out clipped/ --clip national_boundary.gpkg
```

## How it works

1. Scans the input directory for files with extensions `.gpkg`, `.geojson`, `.json`, or `.shp`
2. Applies the operation to each file
3. Writes results to the output directory with the same filename
4. Reports success/failure for each file

Output example:

```
Processing 5 files with operation 'reproject' ...
  OK parcels.gpkg
  OK roads.gpkg
  OK buildings.gpkg
  FAIL boundaries.gpkg: Input dataset has no CRS.
  OK rivers.gpkg

4/5 files processed -> data_clean/
```

## Python equivalent

For more control, use a Python script:

```python
from pathlib import Path
from sudapy.vector.ops import reproject

input_dir = Path("data_raw")
output_dir = Path("data_clean")
output_dir.mkdir(exist_ok=True)

for f in input_dir.glob("*.gpkg"):
    try:
        reproject(f, to_epsg=32636, out=output_dir / f.name)
        print(f"OK {f.name}")
    except Exception as e:
        print(f"FAIL {f.name}: {e}")
```
