import streamlit as st
import requests
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

# Set up the Streamlit page
st.set_page_config(layout="wide")
st.title("Daily Top 5 Marketing News Flashcards for India")

# Sidebar for API key input
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your Google AI Studio API Key", type="password")

# Function to fetch top marketing news
def fetch_top_marketing_news(api_key):
    url = "https://ai.google.com/api/news"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"category": "marketing", "country": "IN", "limit": 5}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        st.error("Failed to fetch news")
        return []

# Function to create flashcards
def create_flashcard(news_item, index):
    img = Image.new('RGB', (400, 300), color=(73, 109, 137))
    d = ImageDraw.Draw(img)

    # Use a sketch font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Title
    title = news_item.get("title", "No Title")
    title = textwrap.fill(title, width=30)
    d.text((20, 20), title, fill=(255, 255, 255), font=font)

    # Description
    description = news_item.get("description", "No Description")
    description = textwrap.fill(description, width=40)
    d.text((20, 100), description, fill=(255, 255, 255), font=font)

    # Source
    source = news_item.get("source", {}).get("name", "Unknown Source")
    d.text((20, 250), f"Source: {source}", fill=(255, 255, 255), font=font)

    return img

# Main application logic
if api_key:
    news_articles = fetch_top_marketing_news(api_key)
    if news_articles:
        st.subheader("Top 5 Marketing News Flashcards")
        cols = st.columns(2)
        for index, news_item in enumerate(news_articles):
            with cols[index % 2]:
                flashcard = create_flashcard(news_item, index)
                st.image(flashcard, caption=f"News {index + 1}", use_column_width=True)

                # Download button
                img_byte_arr = io.BytesIO()
                flashcard.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                st.download_button(
                    label=f"Download Flashcard {index + 1}",
                    data=img_byte_arr,
                    file_name=f"flashcard_{index + 1}.png",
                    mime="image/png"
                )
    else:
        st.warning("No news articles found.")
else:
    st.warning("Please enter your Google AI Studio API Key in the sidebar.")

# LinkedIn post content
linkedin_post = """
📢 Daily Top 5 Marketing News Flashcards for India 📢

Stay updated with the latest marketing trends and news in India with our daily top 5 marketing news flashcards! 🌟

🔹 Each flashcard provides a crisp summary of the most important marketing news.
🔹 Designed with sketch fonts for a unique and engaging visual experience.
🔹 Downloadable images for easy sharing and offline reading.

📲 Try it out now and never miss out on the latest marketing insights! 🚀

#MarketingNews #IndiaMarketing #Flashcards #DigitalMarketing #MarketingTrends #StayUpdated
"""

st.subheader("LinkedIn Post Content")
st.text_area("LinkedIn Post", linkedin_post, height=200)
