# Customer Order Entry System

## Project Overview
This project is a customer order entry application built with Python, Streamlit, and Supabase. It allows users to view customer and product information, create orders, and review order history.

## Features
- Password-protected application access
- View customer and product information
- Select customers and products
- Enter order quantities
- Calculate order totals
- Review and confirm orders before submission
- Save orders to a Supabase database
- View recent order history

## Technologies Used
- Python
- Streamlit
- Supabase
- SQL
- GitHub

## Installation

1. Clone this repository.
2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project folder with your Supabase credentials:

   ```text
   SUPABASE_URL=your_supabase_url
   SUPABASE_SECRET_KEY=your_supabase_secret_key
   APP_PASSWORD=your_app_password
   ```

4. Start the application:

   ```bash
   streamlit run app.py
   ```

## Database
The application uses Supabase to store customer, product, and order information.

## Security
Credentials are stored in a local `.env` file and should never be uploaded to GitHub.
