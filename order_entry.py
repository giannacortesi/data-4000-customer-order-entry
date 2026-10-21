"""Interactive customer order entry and verification."""

from datetime import date
from decimal import Decimal, InvalidOperation

from database import get_client, get_customers, get_products, create_order


def display_customers(customers):
    print("\nCUSTOMERS")
    print(f"{'Customer ID':<15}{'Customer Name'}")
    print("-" * 40)
    for customer in customers:
        print(f"{customer['customer_id']:<15}{customer['name']}")


def display_products(products):
    print("\nPRODUCTS")
    print(f"{'Product ID':<12}{'Product Name':<30}{'Price':>12}")
    print("-" * 54)
    for product in products:
        print(
            f"{product['product_id']:<12}"
            f"{product['product_name']:<30}"
            f"${Decimal(str(product['price'])):>10.2f}"
        )


def get_valid_id(prompt, records, id_field):
    valid_ids = {int(record[id_field]) for record in records}

    while True:
        answer = input(prompt).strip()
        try:
            record_id = int(answer)
        except ValueError:
            print("Please enter a whole-number ID.")
            continue

        if record_id not in valid_ids:
            print("That ID does not exist. Please choose an ID from the table.")
            continue

        return record_id


def get_valid_quantity():
    while True:
        answer = input("Enter quantity: ").strip()

        try:
            quantity = int(answer)
        except ValueError:
            print("Enter a positive whole number, such as 1 or 3.")
            continue

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            continue

        return quantity


def get_confirmation():
    while True:
        answer = input("Save this order? Enter Y or N: ").strip().lower()

        if answer in ("y", "n"):
            return answer == "y"

        print("Please enter Y for yes or N for no.")


def related_record(value):
    """Handle a related record returned as a dictionary or list."""
    if isinstance(value, list):
        return value[0] if value else {}
    return value if isinstance(value, dict) else {}


def display_saved_order(order):
    customer = related_record(order.get("customers"))
    product = related_record(order.get("products"))

    quantity = int(order["quantity"])
    unit_price = Decimal(str(order["unit_price"]))
    total = quantity * unit_price

    print("\nVERIFIED ORDER — RETRIEVED FROM SUPABASE")
    print("-" * 105)
    print(
        f"{'Order ID':<10}"
        f"{'Customer':<22}"
        f"{'Product':<27}"
        f"{'Quantity':>10}"
        f"{'Unit Price':>13}"
        f"{'Total':>11}"
        f"  {'Order Date':<12}"
    )
    print("-" * 105)
    print(
        f"{order['order_id']:<10}"
        f"{customer.get('name', 'Unknown'):<22}"
        f"{product.get('product_name', 'Unknown'):<27}"
        f"{quantity:>10}"
        f"${unit_price:>11.2f}"
        f"${total:>10.2f}"
        f"  {order.get('order_date', ''):<12}"
    )


def enter_order():
    customers = get_customers()
    products = get_products()

    if not customers:
        print("No customers were found in Supabase.")
        return
    if not products:
        print("No products were found in Supabase.")
        return

    display_customers(customers)
    display_products(products)

    customer_id = get_valid_id(
        "\nEnter customer ID: ", customers, "customer_id"
    )
    product_id = get_valid_id(
        "Enter product ID: ", products, "product_id"
    )
    quantity = get_valid_quantity()

    customer = next(
        c for c in customers if int(c["customer_id"]) == customer_id
    )
    product = next(
        p for p in products if int(p["product_id"]) == product_id
    )

    unit_price = Decimal(str(product["price"]))
    total = unit_price * quantity

    print("\nORDER SUMMARY")
    print(f"Customer:   {customer['name']}")
    print(f"Product:    {product['product_name']}")
    print(f"Quantity:   {quantity}")
    print(f"Unit price: ${unit_price:.2f}")
    print(f"Order total: ${total:.2f}")

    if not get_confirmation():
        print("Order cancelled. Nothing was inserted.")
        return

    try:
        # create_order inserts the order and returns its generated order ID.
        saved_order = create_order(customer_id, product_id, quantity)
        order_id = saved_order["order_id"]
        print(f"\nOrder {order_id} was inserted successfully.")

    except Exception:
        print(
            "The order could not be saved. Check your connection, "
            "table permissions, and database setup. No credentials "
            "are displayed."
        )
        return

    try:
        # Make a NEW Supabase request to verify the saved order.
        result = (
            get_client()
            .table("orders")
            .select("*, customers(name, city), products(product_name)")
            .eq("order_id", order_id)
            .execute()
        )

        if not result.data:
            print(
                "The order was inserted, but verification returned "
                "no matching order. Do not submit it again automatically."
            )
            return

        display_saved_order(result.data[0])

    except Exception:
        print(
            "The order was inserted, but verification could not be "
            "completed. Check Supabase before trying another insertion."
        )


def main():
    while True:
        try:
            enter_order()
        except Exception:
            print(
                "Could not complete this operation. Check your Supabase "
                "connection and table setup. No credentials are displayed."
            )

        while True:
            again = input("\nEnter another order? (Y/N): ").strip().lower()
            if again in ("y", "n"):
                break
            print("Please enter Y or N.")

        if again == "n":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
