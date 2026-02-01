"""SudaPy: A Sudan-focused Python toolkit for Geomatics.

Provides GIS, remote sensing, and surveying workflows optimized
for professionals working in Sudan and the surrounding region.
"""

import platform
import struct
import warnings

__version__ = "1.2.1"
__all__ = ["__version__"]

if platform.system() == "Windows" and struct.calcsize("P") * 8 == 32:
    warnings.warn(
        "SudaPy is running on 32-bit Windows. "
        "Core CRS functions work, but geospatial extras ([geo], [viz]) "
        "require 64-bit Windows. Consider switching to a 64-bit Python install.",
        RuntimeWarning,
        stacklevel=2,
    )
