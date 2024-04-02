import string

from django.core.management.base import BaseCommand
import random
from delivery.models import Cars, Locations

class Command(BaseCommand):
    help = 'Загрузка 20 рандомных машин в БД'

    def handle(self, *args, **kwargs):
        if Cars.objects.count() == 0:
            self.stdout.write(self.style.SUCCESS('Загрузка 20 случайных машин...'))
            car_numbers = []
            while len(car_numbers) != 20:
                first_part = ''.join(random.choices(string.digits, k=4))
                second_part = random.choice(string.ascii_uppercase)
                car_number = f"{first_part}{second_part}"
                if car_number not in car_numbers:
                    car_numbers.append(car_number)

            for car in car_numbers:
                capacity = random.randint(1, 1000)
                # current_location = Locations.objects.order_by('?').first()

                car = Cars(car_number=car, capacity=capacity)
                car.save()

            self.stdout.write(self.style.SUCCESS('Машины успешно загружены'))