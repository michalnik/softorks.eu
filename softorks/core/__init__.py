"""Shared, site-wide Django functionality."""

import zlib
from importlib.metadata import version

PROJECT_VERSION = version("softorks.eu")
VERSION_HASH = f"{zlib.crc32(PROJECT_VERSION.encode()):08x}"[:6]
