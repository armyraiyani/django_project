import requests
from django.core.management.base import BaseCommand
from coun.models import Country


class Command(BaseCommand):
    help = "Load only independent countries"

    def handle(self, *args, **kwargs):
        response = requests.get(
            "https://restcountries.com/v3.1/all?fields=name,cca2,idd,currencies,independent"
        )

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"API Error: {response.status_code}"))
            return

        data = response.json()

        for item in data:

            # filter only real countries
            if not item.get("independent"):
                continue

            name = item.get("name", {}).get("common")
            country_code = item.get("cca2")

            dial_code = None
            idd = item.get("idd", {})
            root = idd.get("root")
            suffixes = idd.get("suffixes")

            if root and suffixes:
                dial_code = root + suffixes[0]

            currency_code = None
            currencies = item.get("currencies")
            if currencies:
                currency_code = list(currencies.keys())[0]

            if name and country_code:
                Country.objects.update_or_create(
                    country_code=country_code,
                    defaults={
                        "name": name,
                        "dial_code": dial_code,
                        "currency_code": currency_code,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Independent countries inserted successfully!"))



