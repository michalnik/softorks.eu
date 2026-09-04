import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand, CommandError

from core import VERSION_HASH

VERSION_URL = "https://api.cdnjs.com/libraries/{library}?fields=versions"
FILE_URL = "https://cdnjs.cloudflare.com/ajax/libs/{library}/{version}/{filename}"


class Command(BaseCommand):
    help = "Update configured vendored static assets."

    def add_arguments(self, parser):
        parser.add_argument(
            "--lib-versions",
            metavar="LIBRARY",
            help="Print the versions cdnjs provides for LIBRARY.",
        )

    def handle(self, *args, **options):
        library = options["lib_versions"]
        if library:
            versions = self.get_versions(library)
            available_versions = ", ".join(versions)
            self.stdout.write(
                self.style.SUCCESS(library)
                + self.style.NOTICE(" available versions: ")
                + self.style.HTTP_SUCCESS(available_versions)
            )
            return

    def get_versions(self, library: str) -> list[str]:
        """Return every version cdnjs publishes for ``library``."""
        url = VERSION_URL.format(library=quote(library, safe="-._"))
        request = Request(
            url,
            headers={"User-Agent": f"softorks-static-update/{VERSION_HASH}"},
        )

        try:
            with urlopen(request, timeout=30) as response:  # noqa: S310
                payload = json.load(response)
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            raise CommandError(f"Could not get versions for {library!r}: {error}") from error

        versions = payload.get("versions") if isinstance(payload, dict) else None
        if not isinstance(versions, list) or not all(isinstance(version, str) for version in versions):
            raise CommandError(f"cdnjs returned no valid version list for {library!r}.")
        return versions
