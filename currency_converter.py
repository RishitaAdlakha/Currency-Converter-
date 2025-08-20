import requests
import streamlit as st
 
API_KEY = "b46ac003a0737fc53cbac5fb"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest"
 
 
 
def convert_currency(from_currency, to_currency, amount):
    url = f"{BASE_URL}/{from_currency.upper()}"

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        return f"❌ Error: {e}"

    if response.status_code != 200 or data.get('result') != 'success':
        return f"❌ API Error: {data.get('error-type', 'Unknown error')}"

    rates = data.get("conversion_rates", {})
    if to_currency.upper() not in rates:
        return f"❌ Currency code '{to_currency}' not found."

    rate = rates[to_currency.upper()]
    converted = amount * rate
    return f"{amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}"

 
st.title("💱 Currency Converter")

from_currency = st.text_input("Enter FROM currency (e.g. USD)", "USD")
to_currency = st.text_input("Enter TO currency (e.g. INR)", "INR")
amount = st.number_input("Enter amount to convert", min_value=0.0, format="%.2f")

if st.button("Convert"):
    if not from_currency or not to_currency:
        st.error("❗ Please enter both currency codes.")
    elif amount <= 0:
        st.error("❗ Amount must be greater than 0.")
    else:
        result = convert_currency(from_currency, to_currency, amount)
        st.success(result)
