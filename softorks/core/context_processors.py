from . import VERSION_HASH


def current_version(request):
    return {"version": VERSION_HASH}
