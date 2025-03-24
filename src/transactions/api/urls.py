from django.urls import path
from .views import AllMovementsView, MovementView

urlpatterns = [
    path("movements/", AllMovementsView.as_view(), name="all_movements"),
    path("movements/<int:pk>/", MovementView.as_view(), name="movement"),
]