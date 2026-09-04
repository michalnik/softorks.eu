"""Shared, site-wide Django functionality."""

import zlib

from softorks import version


VERSION_HASH = f"{zlib.crc32(version.encode()):08x}"[:6]
