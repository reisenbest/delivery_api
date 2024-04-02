from django_filters import rest_framework as filters
from .models import Cargo


class CargoDetailFilter(filters.FilterSet):
    min_weight = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    max_weight = filters.NumberFilter(field_name='weight', lookup_expr='lte')
    max_distance = filters.NumberFilter(method='filter_max_distance',
                                        label='Distance (укажите максимальное количество'
                                              'миль, от машины до груза (pick-up) чтобы он учитывался в выборке',
                                        )

    class Meta:
        model = Cargo
        fields = ['min_weight', 'max_weight']

    def filter_max_distance(self, queryset, name, value):
        self.request.max_distance = value
        return queryset
