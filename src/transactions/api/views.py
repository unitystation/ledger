
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from transactions.api.serializers import MoneyMovementSerializer
from transactions.models import Movement


class AllMovementsView(ListAPIView):
    serializer_class = MoneyMovementSerializer
    permission_classes = [AllowAny]
    queryset = Movement.objects.all().order_by("-created_at")

class MovementView(RetrieveAPIView):
    serializer_class = MoneyMovementSerializer
    permission_classes = [AllowAny]
    queryset = Movement.objects.all()
