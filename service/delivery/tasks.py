import random
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Cars, Locations



def start_scheduler():
    def update_car_locations():

        all_cars = Cars.objects.all()
        all_locations = list(Locations.objects.all())

        for car in all_cars:
            new_location = random.choice(all_locations)
            car.current_location = new_location
            car.save()
        print('Локация машин обновлена')
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_car_locations, 'interval', minutes=3)
    scheduler.start()




