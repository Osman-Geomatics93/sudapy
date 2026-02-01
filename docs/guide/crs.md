# CRS & Coordinate Systems

SudaPy includes built-in CRS presets tailored for Sudan and a suggestion engine that recommends the correct UTM zone for any coordinate.

## Why CRS matters in Sudan

Sudan spans **UTM zones 34 through 37 North**, covering longitudes from roughly 22 E to 38 E. Choosing the wrong UTM zone leads to significant distortion in area and distance calculations.

Additionally, legacy survey data in Sudan often uses the **Adindan datum** rather than WGS 84. SudaPy includes both WGS 84 and Adindan presets.

## Built-in presets

| EPSG  | Name                    | Region                          |
|-------|-------------------------|---------------------------------|
| 4326  | WGS 84                  | Global (geographic, lat/lon)    |
| 32634 | WGS 84 / UTM zone 34N  | Western Sudan (~18--24 E)       |
| 32635 | WGS 84 / UTM zone 35N  | Central Sudan (~24--30 E)       |
| 32636 | WGS 84 / UTM zone 36N  | Eastern Sudan (~30--36 E)       |
| 32637 | WGS 84 / UTM zone 37N  | Red Sea coast (~36--42 E)       |
| 20135 | Adindan / UTM zone 35N  | Central Sudan (legacy surveys)  |
| 20136 | Adindan / UTM zone 36N  | Eastern Sudan (legacy surveys)  |
| 20137 | Adindan / UTM zone 37N  | Red Sea (legacy surveys)        |

## Suggest the right CRS

### CLI

```bash
# Khartoum (lon 32.5, lat 15.6)
sudapy crs suggest --lon 32.5 --lat 15.6
```

Returns both WGS 84 / UTM zone 36N (EPSG:32636) and Adindan / UTM zone 36N (EPSG:20136).

```bash
# Port Sudan on the Red Sea coast
sudapy crs suggest --lon 37.2 --lat 19.6
```

Returns WGS 84 / UTM zone 37N (EPSG:32637) and Adindan / UTM zone 37N (EPSG:20137).

### Python API

```python
from sudapy.crs.registry import suggest_utm_zone

suggestions = suggest_utm_zone(lon=32.5, lat=15.6)
for s in suggestions:
    print(f"EPSG:{s['epsg']}  {s['name']}  ({s['datum']})")
```

Output:

```
EPSG:32636  WGS 84 / UTM zone 36N  (WGS 84)
EPSG:20136  Adindan / UTM zone 36N  (Adindan)
```

## List all presets

### CLI

```bash
sudapy crs list
```

### Python API

```python
from sudapy.crs.registry import list_presets

for preset in list_presets():
    print(f"EPSG:{preset.epsg}  {preset.name}  ({preset.region})")
```

## Validate an EPSG code

```python
from sudapy.crs.registry import validate_epsg

crs = validate_epsg(32636)
print(crs)  # <CRS: EPSG:32636>
```

If the EPSG code is invalid, a `CRSError` is raised with a helpful hint.

## Adindan vs WGS 84

!!! info "When to use Adindan"
    Use Adindan CRS only when working with **legacy survey data** that was originally collected in the Adindan datum. For new projects, WGS 84 UTM zones are recommended.

The Adindan datum (also called Blue Nile 1958) was the standard geodetic datum used in Sudan for decades. A datum transformation is required when combining Adindan data with modern WGS 84 datasets:

```python
from sudapy.vector.ops import reproject

# Convert legacy Adindan data to WGS 84 / UTM zone 36N
gdf = reproject("legacy_survey.gpkg", to_epsg=32636, out="survey_wgs84.gpkg")
```

!!! warning
    Datum transformations between Adindan and WGS 84 can introduce shifts of several hundred meters depending on the transformation parameters available. Always validate transformed coordinates against known control points.
