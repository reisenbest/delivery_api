from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .validators import validate_car_number, validate_postcode


# Create your models here.

class Locations(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    state = models.CharField(max_length=50, verbose_name='Штат')
    # валидация исходя из содержимого csv файла с локациями
    postcode = models.CharField(max_length=5, verbose_name='почтовый индекс (zip)',
                                unique=True, blank=False, validators=[validate_postcode])
    latitude = models.FloatField(verbose_name="Широта",
                                 validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(verbose_name='Долгота',
                                  validators=[MinValueValidator(-180), MaxValueValidator(180)])

    class Meta:
        verbose_name = 'Локации'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f'ID: {self.pk} | zip-code: {self.postcode}'


class Cargo(models.Model):
    location_pick_up = models.ForeignKey(Locations, on_delete=models.CASCADE,
                                         related_name='location_from',
                                         verbose_name='Место отправления')
    location_delivery = models.ForeignKey(Locations, on_delete=models.CASCADE,
                                          related_name='location_to',
                                          verbose_name='Место доставки', )

    weight = models.PositiveSmallIntegerField(
        verbose_name='Вес груза',
        help_text='Введите вес груза (1-1000)',
        validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание груза')

    class Meta:
        verbose_name = 'Грузы'
        verbose_name_plural = 'Грузы'

    def __str__(self):
        return f'ID: {self.pk}'


class Cars(models.Model):
    car_number = models.CharField(max_length=5, unique=True, blank=False,
                                  verbose_name='Номер машины', validators=[validate_car_number])
    current_location = models.ForeignKey(Locations, on_delete=models.CASCADE,
                                         verbose_name='Текущая локация', blank=True, null=True)
    capacity = models.PositiveSmallIntegerField(
        verbose_name='Грузоподъемность',
        help_text='Введите грузоподъемность автомобиля (1-1000)',
        validators=[MinValueValidator(1), MaxValueValidator(1000)])

    class Meta:
        verbose_name = 'Машины'
        verbose_name_plural = 'Машины'

    def save(self, *args, **kwargs):
        if not self.pk:
            current_location = Locations.objects.order_by('?').first()
            self.current_location = current_location
        super().save(*args, **kwargs)

    def __str__(self):
        return f'ID: {self.pk} | Номер машины: {self.car_number}'
