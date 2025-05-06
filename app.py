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



st.write("Welcome to RetailBot! Ask me about products, prices, or popular items.")
st.write("If you ask about products,please type find or search.")
st.write("If you ask about popular items,please type top or popular")
st.write("Type 'exit' to leave.")
user_query = st.text_input("Ask about products, prices, or popular items:")
while True:
    user_query = st.text_input("Ask your query (type 'exit' to stop):")
    
    if not user_query:
        st.stop()  # Wait for user input


    user_query = user_query.lower()
    if 'exit' in user_query:
        st.success("Thanks for using the assistant!")
    
    if 'search' in user_query or 'find' in user_query:
        keyword = st.text_input("Enter keyword to search products:")
        if keyword:
            results = df_cleaned[df_cleaned['Description'].str.contains(keyword, na=False)]
            st.write(results[['StockCode', 'Description', 'UnitPrice']].drop_duplicates().head(10))

    elif 'price' in user_query or 'range' in user_query:
        min_price = st.number_input("Min price", min_value=0.0, value=0.0)
        max_price = st.number_input("Max price", min_value=0.0, value=10.0)
        if min_price < max_price:
            results = df_cleaned[(df_cleaned['UnitPrice'] >= min_price) & (df_cleaned['UnitPrice'] <= max_price)]
            st.write(results[['Description', 'UnitPrice']].drop_duplicates().head(10))
        else:
            st.warning("Min price should be less than Max price.")
    elif 'top' in user_query or 'popular' in user_query:
        top_items = df_cleaned.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
        st.write(top_items.reset_index())

    else:
        st.warning("Sorry, I didn't understand that. Try using keywords like 'find', 'price', or 'top'.")
