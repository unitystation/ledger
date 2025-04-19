from decimal import Decimal
from django.utils import timezone
from django.db import models


MOVEMENT_TYPES = [
    ("income", "Income"),
    ("expense", "Expense"),
]


class Movement(models.Model):
    """Represents a money movement (income or expense)."""
    type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    description = models.CharField(max_length=560)
    notes = models.TextField(blank=True, null=True)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs) -> None:
        is_new = self._state.adding
        if is_new:
            self.balance_after = Decimal("0.00")  # Placeholder
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.created_at.date()} - {self.type.capitalize()}: ${self.amount_usd} - {self.description}"


class MovementTemplate(models.Model):
    """Represents a template of sort, to automatically create movements that are recurrent in time."""
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    description = models.CharField(max_length=560)
    notes = models.TextField(blank=True, null=True)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
