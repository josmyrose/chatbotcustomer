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
def chatbot():
    print("Welcome to RetailBot! Ask me about products, prices, or popular items.")
    print("If you ask about products,please type find or search.")
    print("If you ask about popular items,please type top or popular")
    print("Type 'exit' to leave.")
    while True:
        user_input = input("\nYou: ").lower()

        if 'exit' in user_input:
            print("Goodbye!")
            break
        elif 'find' in user_input or 'search' in user_input:
            keyword = input("Enter product keyword: ")
            results = search_product(keyword)
            print(results if not results.empty else "No matching products found.")
        elif 'price' in user_input or 'range' in user_input:
            try:
                min_price = float(input("Min price: "))
                max_price = float(input("Max price: "))
                results = products_in_price_range(min_price, max_price)
                print(results if not results.empty else "No products in that price range.")
            except ValueError:
                print("Please enter valid numbers.")
        elif 'top' in user_input or 'popular' in user_input:
            print(top_selling_products())
        else:
            print("Sorry, I didn't understand that. Try asking about products or prices.")

if __name__ == "__main__":
    chatbot()

