from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update configured vendored static assets."

    def handle(self, *args, **options):
        pass
