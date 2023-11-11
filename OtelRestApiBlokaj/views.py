from rest_framework.response import Response
from rest_framework.decorators import api_view

# MiddleWare
from django.contrib.auth.decorators import login_required

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
@login_required(login_url='anasayfa')
def checkstatus(request):

    if request.user.is_authenticated:
        konuk = KonukCheckInveCheckOut.objects.filter(otel__owner = request.user).all()
        konukserilize = CheckinCheckOut(konuk,many=True)

    return Response(konukserilize.data)