from rest_framework import serializers
from .models import Room, Bed, Type


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), required=False)

    class Meta:
        model = Room
        fields = '__all__'


class BedSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), required=False)

    class Meta:
        model = Bed
        fields = '__all__'
