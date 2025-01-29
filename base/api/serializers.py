
from rest_framework import serializers
from base.models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'  # Include all fields from the Room model
