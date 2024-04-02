from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView, get_object_or_404, RetrieveUpdateAPIView
from rest_framework.views import APIView
from .tasks import start_scheduler
from .docs import *
from .models import Cars, Cargo, Locations
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CargoDetailFilter


# Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду);

class CargoCreateAPIView(generics.CreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    @CreateCargoInstance_schema
    def post(self, request, *args, **kwargs):
        '''
        решил именно здесь в качестве параметров запроса передавать пост код ллокации места отправки
        и места получения. можно через сериадлизатор (как я сделаю с машиной ниже)
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        location_from = self.kwargs.get('location_pick_up')
        location_to = self.kwargs.get('location_delivery')

        try:
            location_pick_up = Locations.objects.get(postcode=location_from)
        except Locations.DoesNotExist:
            raise ValidationError(f"Локация с zip-code '{location_from}'не найдена в базе")

        try:
            location_delivery = Locations.objects.get(postcode=location_to)
        except Locations.DoesNotExist:
            raise ValidationError(f"Локация с zip-code '{location_to}' не найдена в базе")

        serializer.save(location_pick_up=location_pick_up, location_delivery=location_delivery)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# - Редактирование груза по ID (вес, описание);  Удаление груза по ID.
class CargoUpdateDeleteAPIView(generics.UpdateAPIView, generics.DestroyAPIView,
                               generics.RetrieveAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    lookup_field = 'pk'

    @GetCargoInstance_schema
    def get(self, request, *args, **kwargs):
        '''

        Получение информации о конкретном грузе по ID
        (локации pick-up, delivery, вес, описание,
        список номеров ВСЕХ машин с расстоянием до выбранного груза);
        '''
        self.serializer_class = CargoDetailSerializer
        return super().get(request, *args, **kwargs)

    @UpdateCargoInstance_schema
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @UpdateCargoInstance_schema
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @DeleteCargoInstance_schema
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль));\
class CargoListAPIView(generics.ListAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CargoDetailFilter

    @GetCargoList_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CarRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    lookup_field = 'pk'

    @GetCar_schema
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @UpdateCar_schema
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

start_scheduler()