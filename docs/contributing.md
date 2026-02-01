# Contributing

Contributions to SudaPy are welcome. This page covers the development setup and workflow.

## Development setup

```bash
git clone https://github.com/Osman-Geomatics93/sudapy.git
cd sudapy
pip install -e ".[dev,all]"
```

## Running tests

```bash
pytest
```

Tests are in the `tests/` directory and cover CRS logic, vector operations, and area calculations.

## Code style

SudaPy uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
ruff check src/ tests/
ruff format src/ tests/
```

Configuration is in `pyproject.toml`:

- Target: Python 3.9
- Line length: 100
- Rules: E, F, W, I, UP, B, SIM

## Type checking

```bash
mypy src/sudapy/
```

## Project structure

```
src/sudapy/
    __init__.py          # Package version
    core/
        errors.py        # Custom exceptions with hints
        logging.py       # Rich-based logging
    cli/
        main.py          # Typer CLI application
    crs/
        registry.py      # Sudan CRS presets and UTM suggestion
    vector/
        ops.py           # Vector geoprocessing
    raster/
        ops.py           # Raster geoprocessing
    viz/
        maps.py          # Quick map visualization
    rs/
        sentinel.py      # Sentinel satellite search & download
tests/
    test_crs.py          # CRS preset and suggestion tests
    test_vector.py       # Vector operation tests
```

## Adding a new CRS preset

Edit `src/sudapy/crs/registry.py` and add a new `CRSPreset` to `SUDAN_CRS_PRESETS`:

```python
CRSPreset(
    epsg=XXXXX,
    name="Name / UTM zone XXN",
    description="Description of coverage area",
    region="Region name",
),
```

If the zone needs Adindan suggestions, add it to the `adindan_map` dict in `suggest_utm_zone()`.

## Adding a new vector operation

1. Add the function to `src/sudapy/vector/ops.py`
2. Add a CLI command in `src/sudapy/cli/main.py` under `vector_app`
3. Add the operation to the `batch` command's dispatch
4. Add tests in `tests/test_vector.py`
5. Document in `docs/guide/vector.md`

## Submitting changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and add tests
4. Run `pytest` and `ruff check src/ tests/`
5. Commit and push
6. Open a pull request against `main`

## CI

GitHub Actions runs on every push and PR:

- Lint with Ruff
- Test matrix: Ubuntu + Windows, Python 3.9 / 3.11 / 3.12
