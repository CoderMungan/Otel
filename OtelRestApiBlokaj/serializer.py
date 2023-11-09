from OtelIcerik.models import KonukCheckInveCheckOut
from rest_framework import serializers

class CheckinCheckOut(serializers.ModelSerializer):

    otel = serializers.StringRelatedField()
    konuk = serializers.StringRelatedField()
    oda = serializers.StringRelatedField()
    title = serializers.CharField(source="oda")
    start = serializers.DateTimeField(source="checkIn")
    end = serializers.DateTimeField(source="checkOut")
    class Meta:
        model = KonukCheckInveCheckOut
        fields = "__all__"