from geopy.distance import geodesic
from rest_framework import serializers
from .models import Cargo, Locations, Cars


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ('weight', 'description')


class CargoDetailSerializer(serializers.ModelSerializer):
    cars = serializers.SerializerMethodField(help_text='количество машин')

    class Meta:
        model = Cargo
        fields = ('id', 'weight', 'description', 'location_pick_up', 'location_delivery', 'cars')

    def get_cars(self, instance):
        '''
        получение списка всех машин, номера машин + расстояние машин до груза (pick-up) в милях
        '''
        cargo_location = (instance.location_pick_up.latitude, instance.location_pick_up.longitude)
        cars = Cars.objects.all()
        cars_list = {}

        for car in cars:
            car_location = (car.current_location.latitude, car.current_location.longitude)
            distance = geodesic(cargo_location, car_location).miles
            cars_list[car.car_number] = distance

        return cars_list


class CargoListSerializer(serializers.ModelSerializer):
    cars_near_to_cargo_450_miles = serializers.SerializerMethodField(help_text='Количество машин, которые на расстоянии'
                                                                               '450 миль или ближе')

    class Meta:
        model = Cargo
        fields = (
        'id', 'weight', 'description', 'location_pick_up', 'location_delivery', 'cars_near_to_cargo_450_miles')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['location_pick_up'] = instance.location_pick_up.postcode
        representation['location_delivery'] = instance.location_delivery.postcode
        return representation

    def get_cars_near_to_cargo_450_miles(self, instance):
        '''
        получение количества машин, расстояние которых до груза по умолчанию <=450 миль
        или указано пользователем верхняя граница
        '''
        distance = self.context['request'].max_distance if hasattr(self.context['request'], 'max_distance') else 450
        cargo_location = (instance.location_pick_up.latitude, instance.location_pick_up.longitude)
        cars_count = 0

        for car in Cars.objects.all():
            car_location = (car.current_location.latitude, car.current_location.longitude)
            distance_between = geodesic(cargo_location, car_location).miles
            if distance_between <= distance:
                cars_count += 1

        return cars_count


class CarsSerializer(serializers.ModelSerializer):
    current_location = serializers.CharField(source='current_location.postcode')

    class Meta:
        model = Cars
        fields = ['id', 'car_number', 'current_location', 'capacity']

    def validate_current_location(self, value):
        try:
            location = Locations.objects.get(postcode=value)
            return location
        except Locations.DoesNotExist:
            raise serializers.ValidationError("Локаций с указанным почтовым кодом не найдено")

    def update(self, instance, validated_data):
        location_instance = validated_data.pop('current_location', None)
        postcode = location_instance['postcode'].postcode
        if postcode:
            try:
                location = Locations.objects.get(postcode=postcode)
                instance.current_location = location
            except Locations.DoesNotExist:
                raise serializers.ValidationError("Локации с указанным zip кодом не существует в базе")

        return super().update(instance, validated_data)
