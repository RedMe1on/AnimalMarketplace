from rest_framework import serializers

from catalogs.models import BreedType


class BreedTypeSerializers(serializers.ModelSerializer):
    """Вывод типов пород"""

    class Meta:
        model = BreedType
        fields = '__all__'

