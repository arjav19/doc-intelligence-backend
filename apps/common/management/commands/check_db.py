from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Tests connection to PostgreSQL'
  
    def handle(self, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version  = cursor.fetchnote()
                self.stdout.write(self.style.SUCCESS(f"Connected to PostgreSQL: {version[0]}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Connection failed: {e}"))
                
