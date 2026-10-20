"""Simple interactive calculator using the original rate card."""
from milkrate import rate_per_litre, payout, validate_entry


def read_number(prompt):
    """Read a numeric value, retrying after invalid text."""
    while True:
        text = input(prompt).strip()
        try:
            return float(text)
        except ValueError:
            print("Invalid input: enter a number, for example 8.5.")


def main():
    """Read one entry and print its rate and payment."""
    farmer_id = input("Farmer ID: ").strip()
    litres = read_number("Litres: ")
    fat = read_number("Fat percentage: ")
    snf = read_number("SNF percentage: ")
    valid, message = validate_entry(litres, fat, snf)
    if not farmer_id:
        print("Farmer ID cannot be empty.")
        return
    if not valid:
        print("Invalid entry:", message)
        return
    rate = rate_per_litre(fat, snf)
    amount = payout(litres, fat, snf)
    print(f"Farmer {farmer_id} | Rate: Rs {rate:.2f}/L | Amount: Rs {amount:.2f}")


if __name__ == "__main__":
    main()
