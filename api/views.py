from django_filters import rest_framework as filters
from .serializers import BroilerSerializer, InventoryWeekSerializer, NotificationSerializer
from .models import Broiler, Account, InventoryWeek, Notification
from .serializers import BroilerSerializer, InventoryWeekSerializer, UserSerializer
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, BroilerSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

from django.views.generic import View

from .constants import *

class BroilerViewSet(viewsets.ModelViewSet):
    queryset = Broiler.objects.all()
    serializer_class = BroilerSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['id',]
    ordering_fields = ['id', '-id']

class InventoryWeekViewSet(viewsets.ModelViewSet):
    queryset = InventoryWeek.objects.all()
    serializer_class = InventoryWeekSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['id',]
    ordering_fields = ['id', '-id']


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['id',]
    ordering_fields = ['id', '-id']


class UserViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['id', 'email', 'username']


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (AllowAny, )
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print("ERROR", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ConcludeWeeklyReport(View):
    def get(self, request, week_id, token, *args, **kwargs):
        try:
            inventory_week = InventoryWeek.objects.get(id=week_id)
            last_inventory_week = InventoryWeek.objects.get(id=week_id - 1)
        except (InventoryWeek.DoesNotExist):
            inventory_week = None
            last_inventory_week = None
        if (inventory_week is not None) and (last_inventory_week is not None):
            user = request.user
            subject = 'Inventory Report for Week ' + week_id
            message = render_to_string('api/weekly_report.html', {'user': user, 'inventory_week': inventory_week, 'last_inventory_week': last_inventory_week})
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email, ])
