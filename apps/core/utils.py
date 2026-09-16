from decimal import Decimal

def format_npr(amount: Decimal | float | int) -> str:
    """Format amount as NPR currency string."""
    if amount is None:
        amount = 0
    val = Decimal(str(amount))
    return f"NPR {val:,.2f}"