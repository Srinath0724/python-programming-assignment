"""Repeatable tests for the original and revised calculators."""
import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import milkrate
import milkrate_seasonal as seasonal


class OriginalCalculatorTests(unittest.TestCase):
    def test_standard_rate(self):
        self.assertEqual(milkrate.rate_per_litre("3.5", "8.5"), Decimal("30.00"))

    def test_above_standard(self):
        self.assertEqual(milkrate.rate_per_litre("4.2", "8.7"), Decimal("33.40"))

    def test_below_standard(self):
        self.assertEqual(milkrate.rate_per_litre("3.1", "8.3"), Decimal("27.80"))

    def test_payout(self):
        self.assertEqual(milkrate.payout("8.5", "4.2", "8.7"), Decimal("283.90"))

    def test_negative_litres_rejected(self):
        with self.assertRaises(ValueError):
            milkrate.payout(-1, "3.5", "8.5")

    def test_fat_bounds(self):
        self.assertTrue(milkrate.validate_entry(1, 2.0, 8.5)[0])
        self.assertTrue(milkrate.validate_entry(1, 7.0, 8.5)[0])
        self.assertFalse(milkrate.validate_entry(1, 1.9, 8.5)[0])
        self.assertFalse(milkrate.validate_entry(1, 7.1, 8.5)[0])


class SeasonalCalculatorTests(unittest.TestCase):
    def test_seasonal_base_rate(self):
        self.assertEqual(seasonal.rate_per_litre("3.5", "8.5", "april"), Decimal("32.00"))

    def test_seasonal_fat_step(self):
        self.assertEqual(seasonal.rate_per_litre("4.2", "8.5", "april"), Decimal("35.15"))

    def test_bonus_threshold_strictly_greater_than_500(self):
        at_threshold = [(500, "3.5", "8.5")]
        over_threshold = [(501, "3.5", "8.5")]
        self.assertEqual(seasonal.farmer_bonus(at_threshold), Decimal("0.00"))
        self.assertEqual(seasonal.farmer_bonus(over_threshold), Decimal("250.50"))

    def test_ten_day_total_bonus(self):
        entries = [(501, "3.5", "8.5")]
        self.assertEqual(seasonal.ten_day_total(entries, "april"), Decimal("16282.50"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
