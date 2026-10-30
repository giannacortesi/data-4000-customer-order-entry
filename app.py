import os
from datetime import date

import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

st.set_page_config(page_title="Customer Order Entry", page_icon="📦", layout="wide")


def get_column(row, choices):
    """Find the first available column from a list of possible names."""
    for column in choices:
        if column in row:
            return column
    return None


def display_name(row, choices, fallback):
    """Create a readable label for a database record."""
    values = [str(row[c]) for c in choices if c in row and row[c] is not None]
    return " ".join(values) if values else f"{fallback} #{row.get('id', '?')}"


st.title("Customer Order Entry")
st.write("Create and review customer orders.")

# Connect to Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = (
    os.getenv("SUPABASE_SECRET_KEY")
    or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    or os.getenv("SUPABASE_KEY")
)
app_password = os.getenv("APP_PASSWORD")

if not supabase_url or not supabase_key:
    st.error(
        "Supabase credentials are missing. Check that your .env file contains "
        "SUPABASE_URL and SUPABASE_SECRET_KEY."
    )
    st.stop()

if app_password:
    entered_password = st.text_input("App password", type="password")
    if entered_password != app_password:
        st.info("Enter your app password to continue.")
        st.stop()

try:
    supabase = create_client(supabase_url, supabase_key)

    customers = supabase.table("customers").select("*").execute().data or []
    products = supabase.table("products").select("*").execute().data or []

except Exception as e:
    st.error(f"Could not load database records: {type(e).__name__}: {e}")
    st.stop()

if not customers:
    st.warning("No customers were found in the customers table.")
    st.stop()

if not products:
    st.warning("No products were found in the products table.")
    st.stop()

customer_id_col = get_column(customers[0], ["id", "customer_id"])
product_id_col = get_column(products[0], ["id", "product_id"])
price_col = get_column(
    products[0], ["unit_price", "price", "product_price", "selling_price"]
)

if not customer_id_col or not product_id_col:
    st.error("Could not identify the customer or product ID columns.")
    st.write("Customer columns:", list(customers[0].keys()))
    st.write("Product columns:", list(products[0].keys()))
    st.stop()

if not price_col:
    st.error("Could not identify the product price column.")
    st.write("Product columns:", list(products[0].keys()))
    st.stop()

customer_name_cols = ["first_name", "last_name"]
if not any(c in customers[0] for c in customer_name_cols):
    customer_name_cols = [
        "customer_name", "name", "full_name", "email"
    ]

product_name_cols = ["product_name", "name", "title", "description"]

customer_labels = [
    display_name(c, customer_name_cols, "Customer") for c in customers
]
product_labels = [
    display_name(p, product_name_cols, "Product") for p in products
]

st.subheader("Create a New Order")

with st.form("order_form"):
    customer_index = st.selectbox(
        "Customer",
        range(len(customers)),
        format_func=lambda i: customer_labels[i],
    )

    product_index = st.selectbox(
        "Product",
        range(len(products)),
        format_func=lambda i: product_labels[i],
    )

    selected_product = products[product_index]
    unit_price = float(selected_product[price_col])

    st.write(f"Unit price: ${unit_price:,.2f}")

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=10000,
        value=1,
        step=1,
    )

    total = unit_price * quantity
    st.write(f"**Order total: ${total:,.2f}**")

    confirmed = st.checkbox("I have reviewed and confirm this order.")

    submitted = st.form_submit_button("Submit Order", type="primary")

if submitted:
    if not confirmed:
        st.warning("Please check the confirmation box before submitting.")
    else:
        customer = customers[customer_index]
        product = products[product_index]

        order_data = {
            "customer_id": customer[customer_id_col],
            "product_id": product[product_id_col],
            "quantity": int(quantity),
            "unit_price": unit_price,
            "order_date": date.today().isoformat(),
        }

        try:
            result = supabase.table("orders").insert(order_data).execute()

            if result.data:
                st.success("Order submitted successfully!")
                st.write("**Order details**")
                st.write(f"Customer: {customer_labels[customer_index]}")
                st.write(f"Product: {product_labels[product_index]}")
                st.write(f"Quantity: {quantity}")
                st.write(f"Unit price: ${unit_price:,.2f}")
                st.write(f"Total: ${total:,.2f}")
                st.dataframe(result.data, use_container_width=True)
            else:
                st.warning(
                    "The database returned no order details. "
                    "Check the orders table before attempting another submission."
                )

        except Exception as e:
            st.error(f"Order submission error: {type(e).__name__}: {e}")
            st.warning(
                "Check the orders table before retrying, in case the order "
                "was saved despite the error."
            )

st.divider()
st.subheader("Recent Orders")

if st.button("Refresh Order History"):
    try:
        orders = (
            supabase.table("orders")
            .select("*")
            .order("order_date", desc=True)
            .limit(50)
            .execute()
            .data
            or []
        )

        if orders:
            st.dataframe(orders, use_container_width=True)
        else:
            st.info("No orders were found.")

    except Exception as e:
        st.error(f"Could not load order history: {type(e).__name__}: {e}")