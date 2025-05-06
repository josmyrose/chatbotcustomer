import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv('online_retail_cleaned.csv') 
df_cleaned = load_data()
def search_product(keyword):
    keyword = keyword.lower()
    results = df_cleaned[df_cleaned['Description'].str.contains(keyword, na=False)]
    return results[['StockCode', 'Description', 'UnitPrice']].drop_duplicates().head(10)
def products_in_price_range(min_price, max_price):
    results = df_cleaned[(df_cleaned['UnitPrice'] >= min_price) & (df_cleaned['UnitPrice'] <= max_price)]
    return results[['Description', 'UnitPrice']].drop_duplicates().head(10)
def top_selling_products():
    top_items = df_cleaned.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
    return top_items.reset_index()
st.title("🛍️ RetailBot - Product Assistant")

# Maintain chat history
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask me about products, prices, or popular items:")

st.write("Welcome to RetailBot! Ask me about products, prices, or popular items.")
st.write("If you ask about products,please type find or search.")
st.write("If you ask about popular items,please type top or popular")
st.text_input("Type 'exit' to leave.")
    # Streamlit UI

while True:
        user_input = st.text_input("\nYou: ").lower()

        if 'exit' in user_input:
            st.write("Goodbye!")
            break
        elif 'find' in user_input or 'search' in user_input:
            keyword = st.text_input("Enter product keyword: ")
            results = search_product(keyword)
            st.write(results if not results.empty else "No matching products found.")
        elif 'price' in user_input or 'range' in user_input:
            try:
                min_price = float(input("Min price: "))
                max_price = float(input("Max price: "))
                results = products_in_price_range(min_price, max_price)
                st.write(results if not results.empty else "No products in that price range.")
            except ValueError:
                st.write("Please enter valid numbers.")
        elif 'top' in user_input or 'popular' in user_input:
            st.write(top_selling_products())
        else:
            st.write("Sorry, I didn't understand that. Try asking about products or prices.")


