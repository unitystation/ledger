from decimal import Decimal

from django.utils import timezone

from django.db import models


def recalculate_balances():
    """Recalculate the balance after each movement. This way the balance is updated even if you add a movement that happened in the past."""

    movements = Movement.objects.all().order_by("created_at")
    balance = Decimal('0.00')

    for movement in movements:
        if movement.type == 'income':
            balance += movement.amount_usd
        else:
            balance -= movement.amount_usd

        if movement.balance_after != balance:
            movement.balance_after = balance
            movement.save(update_fields=['balance_after'])

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

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if is_new:
            # Temporarily set balance_after to 0 to avoid NULL error
            self.balance_after = Decimal("0.00")

        super().save(*args, **kwargs)  # Save once so the row exists (with a temporary value)
        recalculate_balances()

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
