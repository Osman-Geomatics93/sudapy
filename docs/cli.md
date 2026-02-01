# CLI Reference

## Global

```
sudapy --help
sudapy info
```

## CRS

```
sudapy crs list
sudapy crs suggest --lon <x> --lat <y>
```

## Vector

```
sudapy vector reproject --in <path> --out <path> --to <EPSG>
sudapy vector clip --in <path> --clip <path> --out <path>
sudapy vector dissolve --in <path> --by <field> --out <path>
sudapy vector area --in <path> --field <name> --out <path>
```

## Raster

```
sudapy raster clip --in <path> --clip <path> --out <path>
sudapy raster reproject --in <path> --out <path> --to <EPSG>
```

## Map

```
sudapy map quick --in <path> --out <path.png|path.html>
```
