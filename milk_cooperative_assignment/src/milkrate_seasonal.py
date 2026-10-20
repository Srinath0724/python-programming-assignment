"""Revised seasonal milk payment calculator for Task 12."""
from decimal import Decimal, ROUND_HALF_UP

STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
STEP_SIZE = Decimal("0.1")
SNF_STEP_VALUE = Decimal("0.30")  # Assumption: original SNF value is retained.
BONUS_RATE = Decimal("0.50")
BONUS_THRESHOLD_LITRES = Decimal("500")


def rate_card(season):
    """Select the rate card for a season; April-June uses the seasonal card."""
    season = season.strip().lower()
    if season in {"april", "may", "june"}:
        return {
            "base": Decimal("32.00"),
            "fat_step": Decimal("0.45"),
            "snf_step": SNF_STEP_VALUE,
        }
    return {
        "base": Decimal("30.00"),
        "fat_step": Decimal("0.40"),
        "snf_step": SNF_STEP_VALUE,
    }


def nearest_whole_step(reading, standard):
    """Round a reading's number of 0.1 steps to the nearest whole step."""
    steps = (Decimal(str(reading)) - standard) / STEP_SIZE
    return int(steps.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def rate_per_litre(fat, snf, season="regular"):
    """Calculate the per-litre rate using the selected seasonal rate card."""
    card = rate_card(season)
    fat_steps = nearest_whole_step(fat, STANDARD_FAT)
    snf_steps = nearest_whole_step(snf, STANDARD_SNF)
    value = card["base"] + fat_steps * card["fat_step"] + snf_steps * card["snf_step"]
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def ten_day_total_litres(entries):
    """Return the total litres across entries shaped as (litres, fat, snf)."""
    return sum((Decimal(str(entry[0])) for entry in entries), Decimal("0"))


def farmer_bonus(entries):
    """Return the bonus for ten-day supply greater than 500 litres."""
    litres = ten_day_total_litres(entries)
    if litres > BONUS_THRESHOLD_LITRES:
        return (litres * BONUS_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return Decimal("0.00")


def payout(litres, fat, snf, season="regular"):
    """Return the payment for a single entry, before any ten-day bonus."""
    amount = Decimal(str(litres)) * rate_per_litre(fat, snf, season)
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def ten_day_total(entries, season="regular"):
    """Return entry payments plus the qualifying ten-day bonus."""
    base_total = sum(
        (payout(litres, fat, snf, season) for litres, fat, snf in entries),
        Decimal("0.00"),
    )
    return (base_total + farmer_bonus(entries)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


def main():
    """Demonstrate regular and seasonal calculations."""
    entries = [(200, "4.20", "8.70"), (180, "3.50", "8.50"), (130, "3.10", "8.30")]
    print("Total litres:", ten_day_total_litres(entries))
    print("Regular total:", ten_day_total(entries, "regular"))
    print("April-June total (includes bonus if eligible):", ten_day_total(entries, "april"))


if __name__ == "__main__":
    main()
