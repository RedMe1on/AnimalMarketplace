import django_filters as filters

from catalogs.models import BreedType


class BreedTypeFilter(filters.FilterSet):
    class Meta:
        model = BreedType
        fields = ('category',)
