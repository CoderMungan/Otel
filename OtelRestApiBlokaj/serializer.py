from OtelIcerik.models import KonukCheckInveCheckOut
from rest_framework import serializers

class CheckinCheckOut(serializers.ModelSerializer):

    otel = serializers.StringRelatedField()
    konuk = serializers.StringRelatedField()
    oda = serializers.StringRelatedField()
    class Meta:
        model = KonukCheckInveCheckOut
        fields = "__all__"