"""Milk cooperative payment calculations.

Original rate card:
- Base rate: Rs 30.00 per litre at 3.5% fat and 8.5% SNF.
- Each 0.1 percentage-point fat step changes the rate by Rs 0.40.
- Each 0.1 percentage-point SNF step changes the rate by Rs 0.30.
"""
from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
STEP_SIZE = Decimal("0.1")


def nearest_whole_step(reading, standard):
    """Return the nearest whole 0.1-percentage-point step from standard."""
    difference = Decimal(str(reading)) - standard
    steps = difference / STEP_SIZE
    return int(steps.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def rate_per_litre(fat, snf):
    """Return the original rate per litre, rounded to two decimal places."""
    fat_steps = nearest_whole_step(fat, STANDARD_FAT)
    snf_steps = nearest_whole_step(snf, STANDARD_SNF)
    rate = BASE_RATE + Decimal(fat_steps) * FAT_STEP_VALUE + Decimal(snf_steps) * SNF_STEP_VALUE
    return rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def payout(litres, fat, snf):
    """Return the amount payable for one milk delivery, rounded to paise."""
    litres_d = Decimal(str(litres))
    if litres_d < 0:
        raise ValueError("Litres cannot be negative.")
    return (litres_d * rate_per_litre(fat, snf)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


def ten_day_total(entries):
    """Return the sum of payment amounts for a farmer's ten-day entries."""
    return sum((payout(litres, fat, snf) for litres, fat, snf in entries), Decimal("0.00"))


def validate_entry(litres, fat, snf):
    """Validate litres and milk quality readings; return (valid, message)."""
    try:
        litres_d, fat_d, snf_d = Decimal(str(litres)), Decimal(str(fat)), Decimal(str(snf))
    except Exception:
        return False, "Litres, fat and SNF must be numeric."
    if not all(v.is_finite() for v in (litres_d, fat_d, snf_d)):
        return False, "Values must be finite numbers."
    if litres_d < 0:
        return False, "Litres cannot be negative."
    if not Decimal("2.0") <= fat_d <= Decimal("7.0"):
        return False, "Fat must be between 2.0% and 7.0%."
    if not Decimal("0.0") <= snf_d <= Decimal("12.0"):
        return False, "SNF must be between 0.0% and 12.0%."
    return True, "Valid entry."


def main():
    """Run sample calculations when this module is executed directly."""
    examples = [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]
    for litres, fat, snf in examples:
        rate = rate_per_litre(fat, snf)
        amount = payout(litres, fat, snf)
        print(f"{litres:5} L fat {fat} snf {snf} rate {rate:.2f} pay {amount:.2f}")


if __name__ == "__main__":
    main()
