import csv
from django.core.management.base import BaseCommand
from delivery.models import Locations

class Command(BaseCommand):
    help = 'Загрузка локаций из csv файла'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к CSV файлу')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Загрузка локаций...'))
        file_path = options['file_path']
        self.load_locations_from_csv(file_path)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))

    def load_locations_from_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                city = row['city']
                state = row['state_name']
                postcode = row['zip']
                latitude = float(row['lat'])
                longitude = float(row['lng'])
                location, created = Locations.objects.get_or_create(postcode=postcode,
                                                                    defaults={
                                                                        'city': city,
                                                                        'state': state,
                                                                        'latitude': latitude,
                                                                        'longitude': longitude,
                                                                    }
                                                                    )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Локация создана: {location}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Локация уже существует: {location}'))
                
