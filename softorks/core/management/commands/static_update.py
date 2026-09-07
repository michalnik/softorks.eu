import json
from collections.abc import Iterator
from pathlib import Path
from typing import override
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core import VERSION_HASH

VERSION_URL = "https://api.cdnjs.com/libraries/{library}?fields=versions"
FILE_URL = "https://cdnjs.cloudflare.com/ajax/libs/{library}/{version}/{filename}"


class Command(BaseCommand):
    help = "Update configured vendored static assets."

    @override
    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="subcommand")
        subparsers.add_parser(
            "parse-settings",
            help="Print the static-update library configuration.",
        )
        lib_versions_parser = subparsers.add_parser(
            "lib-versions",
            help="Print the versions cdnjs provides for a library.",
        )
        lib_versions_parser.add_argument(
            "library",
            metavar="LIBRARY",
            help="The cdnjs library name.",
        )
        range_options = lib_versions_parser.add_mutually_exclusive_group()
        range_options.add_argument(
            "--max-version",
            metavar="MIN-MAX",
            help="Print the maximum available version in the MIN-MAX range.",
        )
        range_options.add_argument(
            "--in-range",
            metavar="MIN-MAX",
            help="Print the available versions in the MIN-MAX range.",
        )

    @override
    def handle(self, *args, **options):  # noqa: C901 (6)
        if options["subcommand"] == "parse-settings":
            for library, version_range, files in self.get_configured_libraries():
                self.stdout.write(
                    self.style.SUCCESS(library)
                    + self.style.NOTICE(" version range: ")
                    + self.style.SUCCESS(str(version_range))
                    + self.style.NOTICE(" files: ")
                    + self.style.SUCCESS(str(files))
                )
            return

        if options["subcommand"] == "lib-versions":
            library = options["library"]
            maximum_version = options["max_version"]
            versions_in_range = options["in_range"]
            if maximum_version:
                version_range = self.parse_version_range(maximum_version)
                available_version = self.get_max_version(library, version_range)
                self.stdout.write(
                    self.style.SUCCESS(library)
                    + self.style.NOTICE(" maximum available version number: ")
                    + self.style.HTTP_SUCCESS(available_version)
                )
                return

            if versions_in_range:
                version_range = self.parse_version_range(versions_in_range)
                versions = self.get_versions_in_range(library, version_range)
                available_versions = ", ".join(versions)
                self.stdout.write(
                    self.style.SUCCESS(library)
                    + self.style.NOTICE(f" available versions in range {versions_in_range}: ")
                    + self.style.HTTP_SUCCESS(available_versions)
                )
                return

            versions = self.get_versions(library)
            available_versions = ", ".join(versions)
            self.stdout.write(
                self.style.SUCCESS(library)
                + self.style.NOTICE(" available versions: ")
                + self.style.HTTP_SUCCESS(available_versions)
            )
            return

        downloaded_files = self.download_configured_files()
        for destination, content in downloaded_files.items():
            destination.parent.mkdir(exist_ok=True)
            destination.write_bytes(content)

    def download_configured_files(self) -> dict[Path, bytes]:
        """Download every configured file into memory without changing static files."""
        configured_libraries = list(self.get_configured_libraries())
        static_directory = Path(settings.STATICFILES_DIRS[0]).resolve()
        destinations = {
            destination: self.get_static_file_path(static_directory, destination)
            for _, _, files in configured_libraries
            for destination in files.values()
        }

        downloaded_files: dict[Path, bytes] = {}
        for library, version_range, files in configured_libraries:
            version = self.get_max_version(library, version_range)
            for filename, destination in files.items():
                downloaded_files[destinations[destination]] = self.download_file(
                    library,
                    version,
                    filename,
                )
        return downloaded_files

    @staticmethod
    def get_static_file_path(static_directory: Path, destination: str) -> Path:
        """Return a configured destination within the project static directory."""
        static_file = (static_directory / destination).resolve()
        if not static_file.is_relative_to(static_directory):
            raise CommandError(f"Static destination {destination!r} is outside the static directory.")
        return static_file

    def get_max_version(self, library: str, version_range: dict[str, tuple[int, int, int]]) -> str:
        """Return the greatest stable cdnjs version within ``version_range``."""
        available_versions = self.get_versions_in_range(library, version_range)
        if not available_versions:
            raise CommandError(f"No available {library!r} version matches the requested range.")
        return max(
            available_versions,
            key=self.parse_version_number,
        )

    def get_versions_in_range(self, library: str, version_range: dict[str, tuple[int, int, int]]) -> list[str]:
        minimum = version_range["min"]
        maximum = version_range["max"]
        if minimum >= maximum:
            raise CommandError("The minimum version must be lower than the maximum version.")

        return [
            version
            for version in self.get_versions(library)
            if self.is_stable_version(version) and minimum <= self.parse_version_number(version) < maximum
        ]

    def parse_version_range(self, value: str) -> dict[str, tuple[int, int, int]]:
        """Parse a MIN-MAX command-line value into an inclusive/exclusive range."""
        minimum, separator, maximum = value.partition("-")
        if not separator or not minimum or not maximum:
            raise CommandError("The version range must have the format MIN-MAX.")
        return {
            "min": self.parse_version_number(minimum),
            "max": self.parse_version_number(maximum),
        }

    def get_configured_libraries(  # noqa: C901 (7)
        self,
    ) -> Iterator[tuple[str, dict[str, tuple[int, int, int]], dict[str, str]]]:
        """Yield library name, parsed range, and cdnjs-to-local file mappings."""
        configured_libraries = getattr(settings, "STATIC_UPDATE_LIBRARIES", {})
        if not isinstance(configured_libraries, dict):
            raise CommandError("STATIC_UPDATE_LIBRARIES must be a mapping.")

        for library, configuration in configured_libraries.items():
            if not isinstance(library, str) or not library:
                raise CommandError("Each static-update library name must be a non-empty string.")
            if not isinstance(configuration, dict):
                raise CommandError(f"The configuration for {library!r} must be a mapping.")

            version_range = configuration.get("version_range")
            files = configuration.get("files")
            if not isinstance(version_range, str):
                raise CommandError(f"The version range for {library!r} must be a string.")
            if not isinstance(files, dict) or not all(
                isinstance(source, str) and isinstance(destination, str) for source, destination in files.items()
            ):
                raise CommandError(f"The files for {library!r} must be a string mapping.")

            yield library, self.parse_version_range(version_range), files

    @staticmethod
    def is_stable_version(value: str) -> bool:
        return len(value.split(".")) == 3 and all(part.isdigit() for part in value.split("."))

    @staticmethod
    def parse_version_number(value: str | None) -> tuple[int, int, int]:
        if not isinstance(value, str):
            raise CommandError("The library version must have the format X.Y or X.Y.Z.")

        parts = value.split(".")
        if len(parts) == 2:
            parts.append("0")

        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            raise CommandError("The library version must have the format X.Y or X.Y.Z.")

        major, minor, patch = (int(part) for part in parts)
        return major, minor, patch

    @staticmethod
    def get_versions(library: str) -> list[str]:
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

    @staticmethod
    def download_file(library: str, version: str, filename: str) -> bytes:
        """Download one versioned cdnjs file."""
        url = FILE_URL.format(
            library=quote(library, safe="-._"),
            version=quote(version, safe="-._"),
            filename=quote(filename, safe="/-._"),
        )
        request = Request(
            url,
            headers={"User-Agent": f"softorks-static-update/{VERSION_HASH}"},
        )

        try:
            with urlopen(request, timeout=30) as response:
                return response.read()
        except (URLError, TimeoutError) as error:
            raise CommandError(f"Could not download {filename!r} from {library!r}: {error}") from error
