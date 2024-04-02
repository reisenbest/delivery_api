from .serializers import CargoSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

CreateCargoInstance_schema = swagger_auto_schema(
    operation_summary="Создание нового груза (характеристики локаций pick-up, delivery определяются "
                      "по введенному zip-коду) передаю через параметры запроса;",
    operation_description='решил именно здесь в качестве параметров запроса передавать пост код ллокации '
                          'места отправкии места получения. можно через сериадлизатор (как я сделаю с машиной ниже)',
    tags=["Грузы"],
    responses={
        201: "Груз создан",
    },
    request_body=CargoSerializer,
    manual_parameters=[
        openapi.Parameter('location_pick_up', openapi.IN_PATH, description="zip-code места отправления",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('location_delivery', openapi.IN_PATH, description="zip-code места доставки",
                          type=openapi.TYPE_STRING),
    ],
)

UpdateCargoInstance_schema = swagger_auto_schema(
    operation_summary="Редактирование груза по ID (вес, описание);",
    tags=["Грузы"],
    responses={200: "Груз успешно обновлен", 400: "Ошибка валидации данных"},
    request_body=CargoSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="id записи, которую нужно отредактировать",
                          type=openapi.TYPE_STRING), ],
)

DeleteCargoInstance_schema = swagger_auto_schema(
    operation_summary="Удаление груза по ID.",
    tags=["Грузы"],
    responses={
        204: "Груз удален",
    },
    request_body=CargoSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="id записи, которую нужно удалить",
                          type=openapi.TYPE_STRING), ],
)

RetrieveCargoInstance_schema = swagger_auto_schema(
    operation_summary="Получение информации о конкретном грузе по ID (локации pick-up, delivery,"
                      " вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);",
    tags=["Грузы"],
    responses={
        200: "Детальное инфо о грузе",
    },
    request_body=CargoSerializer,
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="id записи, по которой нужно получить инфо",
                          type=openapi.TYPE_STRING), ],
)

GetCargoInstance_schema = swagger_auto_schema(
    operation_summary="Получение информации о конкретном грузе по ID"
                      "Возвращаются данные о локациях pick-up и delivery, "
                      "весе, описании груза и списке номеров всех машин с расстоянием до выбранного груза.",
    responses={200: "Информация о грузе успешно получена"},
    tags=["Грузы"],
)

GetCargoList_schema = swagger_auto_schema(
    operation_summary="Получение списка грузов (локации pick-up, delivery, "
                      "количество ближайших машин до груза ( =< 450 миль)); "
                      "+ фильтры по весу груза и мили ближайших машин до грузов",
    operation_description=" возвращает список грузов вместе с их местами отправления и доставки. "
                          "Также возвращает количество ближайших машин до каждого груза (pick-up)"
                          ", где расстояние до груза меньше или равно 450 миль."
                          "+ фильтры по весу груза и мили ближайших машин до грузов",
    responses={200: "Информация о грузах успешно получена"},
    tags=["Грузы"],
)

UpdateCar_schema = swagger_auto_schema(
    operation_summary="Редактирование машины по ID (локация (определяется по введенному zip-коду));",
    responses={200: "Информация о машине успешно обновлена"},
    tags=["Машины"],
)

GetCar_schema = swagger_auto_schema(
    operation_summary="Получение машины по ID",
    responses={200: "Информация о машине успешно получена"},
    tags=["Машины"],
)
