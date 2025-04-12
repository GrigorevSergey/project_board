from django.core.management import BaseCommand

from accounts.models import Users
from api.models import Board, Project


class Command(BaseCommand):
    help = "Warmup cache"

    def handle(self, *args, **options):
        Project.objects.all().exists()
        Board.objects.all().exists()
        Users.objects.all().exists()

        self.stdout.write("Warmup ok")
