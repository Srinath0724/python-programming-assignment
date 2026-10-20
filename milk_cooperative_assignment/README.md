# Milk Cooperative Payment Calculator — Python Programming Lab

This repository contains example implementations for the milk payment assignment.

## Files
- `src/milkrate.py` — original rate card, payment functions, validation and direct-run demonstration.
- `src/milkrate_seasonal.py` — Task 12 seasonal rate card and ten-day bonus.
- `src/interactive_calculator.py` — interactive single-entry calculator.
- `tests/test_milkrate.py` — repeatable automated tests.
- `evidence/` — place your own terminal screenshots and output captures here.

## Requirements
Python 3.10+ is recommended. The programs use only the Python standard library.

## Run the examples
From the repository root:

```bash
python src/milkrate.py
python src/milkrate_seasonal.py
python -m unittest discover -s tests -v
```

Run the interactive calculator with:

```bash
python src/interactive_calculator.py
```

If your Python installation uses the `py` launcher on Windows, replace `python` with `py`.

## Original rate card
- Base rate = Rs 30.00/L at 3.5% fat and 8.5% SNF.
- Fat step = Rs 0.40/L per nearest 0.1 percentage-point step from 3.5%.
- SNF step = Rs 0.30/L per nearest 0.1 percentage-point step from 8.5%.
- Payment is rounded to two decimal places.

## Task 12 assumptions
- April, May and June use base Rs 32.00/L and fat-step value Rs 0.45.
- The original SNF-step value Rs 0.30 is retained because the changed requirement does not specify a new SNF value.
- The bonus is Rs 0.50 per litre on the entire ten-day volume only when the total is strictly greater than 500 L. At exactly 500 L, no bonus is applied.
- Half-step rounding uses `ROUND_HALF_UP` to make the policy explicit and avoid binary floating-point surprises.

## Important submission note
Run the programs on your own computer and capture your actual terminal outputs. Do not claim screenshots or timings that you have not personally generated. Add screenshots to `evidence/` and commit them to your GitHub repository.
