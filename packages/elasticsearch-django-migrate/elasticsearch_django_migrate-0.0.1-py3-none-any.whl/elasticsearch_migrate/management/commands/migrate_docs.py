from django.core.management.base import BaseCommand
from ...registry import registry


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--reindex', action='store_true', help='Reindex data')

    def handle(self, *args, **options):
        registry.migrate(options['reindex'])
