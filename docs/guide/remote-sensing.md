# Remote Sensing

SudaPy includes helpers for searching and downloading Sentinel satellite imagery via the Copernicus Open Access Hub.

!!! note "Optional dependency"
    Remote sensing features require the `rs` extra: `pip install "sudapy[rs]"`

## Setup

### 1. Install the extra

```bash
pip install "sudapy[rs]"
```

### 2. Set Copernicus credentials

Register at [Copernicus Open Access Hub](https://scihub.copernicus.eu/dhus/#/self-registration), then set environment variables:

=== "Linux / macOS"

    ```bash
    export COPERNICUS_USER=your_username
    export COPERNICUS_PASSWORD=your_password
    ```

=== "Windows (cmd)"

    ```cmd
    set COPERNICUS_USER=your_username
    set COPERNICUS_PASSWORD=your_password
    ```

=== "Windows (PowerShell)"

    ```powershell
    $env:COPERNICUS_USER = "your_username"
    $env:COPERNICUS_PASSWORD = "your_password"
    ```

## Search for scenes

### CLI

```bash
sudapy rs sentinel-search \
    --lon 32.5 --lat 15.6 \
    --start 2025-01-01 --end 2025-06-30 \
    --platform Sentinel-2 \
    --max-cloud 20
```

### Python

```python
from sudapy.rs.sentinel import search_scenes

results = search_scenes(
    lon=32.5,
    lat=15.6,
    start_date="2025-01-01",
    end_date="2025-06-30",
    platform_name="Sentinel-2",
    max_cloud=20,
)

for scene in results[:5]:
    print(f"{scene['date']}  cloud={scene['cloud_cover']:.1f}%  {scene['title']}")
```

### Search parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `lon`, `lat` | (required) | Center point coordinates |
| `start_date`, `end_date` | (required) | Date range as YYYY-MM-DD |
| `platform_name` | `Sentinel-2` | Satellite platform |
| `max_cloud` | `30` | Maximum cloud cover percentage |

### Return format

Each result is a dictionary:

```python
{
    "uuid": "abc123...",
    "title": "S2A_MSIL1C_20250115T...",
    "date": "2025-01-15",
    "cloud_cover": 12.3,
}
```

## Download a scene

### CLI

```bash
sudapy rs sentinel-download --uuid abc123... --out downloads/
```

### Python

```python
from sudapy.rs.sentinel import download_scene

path = download_scene(uuid="abc123...", out_dir="downloads/")
print(f"Downloaded to: {path}")
```

## Workflow example

```bash
# 1. Search for recent low-cloud Sentinel-2 scenes near Khartoum
sudapy rs sentinel-search \
    --lon 32.5 --lat 15.6 \
    --start 2025-01-01 --end 2025-03-31 \
    --max-cloud 10

# 2. Download a specific scene (copy UUID from search results)
sudapy rs sentinel-download --uuid <UUID> --out data_raw/

# 3. Process the downloaded raster
sudapy raster clip --in data_raw/scene.tif --clip study_area.gpkg --out clipped.tif
sudapy raster reproject --in clipped.tif --out scene_utm.tif --to 32636
```
