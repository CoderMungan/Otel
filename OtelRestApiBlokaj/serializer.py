from OtelIcerik.models import KonukCheckInveCheckOut
from rest_framework.serializers import ModelSerializer

class CheckinCheckOut(ModelSerializer):

    class Meta:
        model = KonukCheckInveCheckOut
        fields = "__all__"