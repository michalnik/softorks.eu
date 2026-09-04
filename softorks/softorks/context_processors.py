import zlib
from softorks import version


def current_version(request):
    hash_version = f"{zlib.crc32(version.encode()):08x}"[:6]
    return {"version": hash_version}
