# DATA 4000 — Customer Order Entry


## Project Overview

This project uses Python and the Supabase API to create orders for existing customers. It retrieves customers and products from Supabase, validates user input, displays an order summary, saves confirmed orders, and retrieves saved orders to verify successful insertion.

Each order contains one product and can include multiple units.

## Requirements

- Python 3
- A Supabase project with `customers`, `products`, and `orders` tables
- A valid Supabase project URL and secret key

## Setup

1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Open a terminal in that folder.
4. Install the required packages:

   python3 -m pip install -r requirements.txt

5. Copy `.env.example` to a new file named `.env`.
6. Replace the placeholders in `.env` with your own Supabase project URL and secret key.
7. Keep `.env` private. Never upload it to GitHub.

## How to Run

In the VS Code terminal, run:

    python3 order_entry.py

Follow the prompts to select a customer, select a product, enter a quantity, and confirm or cancel the order.

After an order is confirmed, the program inserts it into Supabase using the current product price and date. It then queries Supabase again using the generated order ID and displays the retrieved order details.

## Input Validation

The program checks that:

- Customer IDs are whole numbers that exist in the database.
- Product IDs are whole numbers that exist in the database.
- Quantity is a positive whole number.
- Confirmation responses are either Y or N.
- Invalid entries display an explanatory message and prompt the user again.

## Testing Results

| Test | Result |
|---|---|
| Text entered as customer ID | Passed |
| Unknown product ID | Passed |
| Quantity of 0 | Passed |
| Negative quantity | Passed |
| Decimal quantity | Passed |
| Text entered as quantity | Passed |
| Order cancelled with N | Passed |
| Valid order confirmed with Y | Passed |
| Newly saved order retrieved from Supabase | Passed |
| Exited the program using N | Passed |

Note: The unknown customer ID test was not separately confirmed.

## Files

- `order_entry.py`: Interactive order entry, validation, confirmation, and verification.
- `database.py`: Reusable Supabase API functions.
- `config.py`: Loads project configuration from `.env`.
- `requirements.txt`: Required Python packages.
- `.env.example`: Example configuration with placeholders only.
- `.gitignore`: Excludes secrets and unnecessary files.
- `README.md`: Project overview, setup instructions, and testing results.

## Learning Resources

- [Supabase Python Client documentation](https://supabase.com/docs/reference/python/introduction)
- [Python documentation](https://docs.python.org/3/)
- [python-dotenv documentation](https://pypi.org/project/python-dotenv/)

## Security

Never commit `.env`, secret keys, or other credentials to the repository. The `.env.example` file should contain placeholders only. Ensure `.gitignore` excludes `.env`.