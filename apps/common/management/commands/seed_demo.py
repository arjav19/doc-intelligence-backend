from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates demo user for quick testing'

    def handle(self, *args, **kwargs):
        user, created =  User.objects.get_or_create(username='demouser',email='demo@example.com')
        if created:
            user.set_password('demo12345')
            user.save()
            self.stdout.write(self.style.SUCCESS("Created demo user : deomuser / demo12345 "))
        else:
            self.stdout.write("Demo user already exists: demouser / demo12345")
                