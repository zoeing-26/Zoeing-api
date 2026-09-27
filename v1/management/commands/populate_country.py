from django.core.management.base import BaseCommand
import pycountry
from v1.models import Country

class Command(BaseCommand):
    def handle(self,*args,**kwargs):

        for country in pycountry.countries:
            Country.objects.get_or_create(
                code = country.alpha_2,
                defaults={'name' : country.name}
            )


        self.stdout.write(self.style.SUCCESS('Done'))
