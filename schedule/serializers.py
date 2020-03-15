from rest_framework import serializers

from .models import Groups


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Groups
        fields = ('name', )
