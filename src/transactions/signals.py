from decimal import Decimal
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Movement
from logging import getLogger

logger = getLogger(__name__)

def recalculate_balances() -> None:
    """Recalculate balances chronologically after each movement."""
    movements = Movement.objects.all().order_by("created_at")
    balance = Decimal('0.00')
    to_update: list[Movement] = []

    for movement in movements.iterator():
        balance += movement.amount_usd if movement.type == 'income' else -movement.amount_usd

        if movement.balance_after != balance:
            movement.balance_after = balance
            to_update.append(movement)

    Movement.objects.bulk_update(to_update, ['balance_after'])


@receiver([post_save, post_delete], sender=Movement)
def movement_changed(
    sender: type[Movement], # noqa
    instance: Movement,
    **kwargs,                # swallows raw, using, signal, etc.
) -> None:
    # Skip when loaddata is running (raw fixture load)
    if kwargs.get("raw"):
        logger.debug("Raw fixture load – balance recomputation skipped")
        return

    logger.info("Updated balance for movement %s", instance)
    try:
        recalculate_balances()
    except Exception as e:
        logger.exception(f"Failed to recalculate balances: {e}")