
import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Book Data Scraping and Analysis App")

url = "https://books.toscrape.com/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

books = soup.select("article.product_pod")

titles = []
prices = []

for book in books:

    title = book.h3.a["title"]

    price = book.select_one(".price_color").text
    price = price.replace("£","").replace("Â","")

    titles.append(title)
    prices.append(float(price))


data = pd.DataFrame({
    "Book Title": titles,
    "Price (£)": prices
})


st.subheader("All Books Data")
st.dataframe(data)


search = st.text_input("Search Book")

if search:
    result = data[data["Book Title"].str.contains(search, case=False)]
    st.write("Search Results")
    st.dataframe(result)


max_price = st.slider("Select Maximum Price", 0, 60, 30)

filtered = data[data["Price (£)"] <= max_price]

st.subheader("Books Under Selected Price")
st.dataframe(filtered)


st.write("Total Books Scraped:", len(data))


st.subheader("Top 5 Expensive Books")

top_books = data.sort_values(by="Price (£)", ascending=False).head(5)

fig, ax = plt.subplots()

ax.bar(top_books["Book Title"], top_books["Price (£)"])

plt.xticks(rotation=45) 

st.pyplot(fig)