from rest_framework.response import Response
from rest_framework.decorators import api_view

from OtelIcerik.models import KonukCheckInveCheckOut
from .serializer import CheckinCheckOut
# Create your views here.

from OtelIcerik.models import *


routes = [

    {
        "route": "checkstatus",
        "description": "tüm checkin ve checkoutları döndürür",
        "methods": "GET" 
    }
]


@api_view(["GET"])
def send_routes(request):

    return Response(routes)


@api_view(["GET"])
def checkstatus(request):

    konuk = KonukCheckInveCheckOut.objects.all()
    konukserilize = CheckinCheckOut(konuk ,many=True)

    return Response(konukserilize.data)