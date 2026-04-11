# import streamlit as st 
# from textblob import TextBlob # Text Processing
# import pandas as pd # Data Manipulation
# import emoji # Emoji Handling
# from bs4 import BeautifulSoup # HTML Parsing
# from urllib.request import urlopen # Web Scraping

# st.set_page_config(page_title="Sentiment Analysis Web App",layout="centered")
# @st.cache_data # Cache the data loading function to improve performance
# def get_text(raw_url): 
#     """
#     Fetches and extracts text from a given URL.
#     Args:
#         raw_url (str): The URL of the webpage to fetch text from.
#         Returns: str: The extracted text from the webpage.
#     """
#     page = urlopen(raw_url) # Open the URL and read the page content
#     soup = BeautifulSoup(page, "html.parser") # Parse the HTML content using BeautifulSoup
#     fetched_text = " ".join(map(lambda p: p.text, soup.find_all('p'))) # Extract text from all paragraph tags and join them into a single string
#     return fetched_text # Return the extracted text
    
# def main():
#     """
#     Sentiment Analysis Web App
#     """
#     st.title("Sentiment Analysis Web App using NLP and ML!") # Set the title of the web app
#     activities = ["Sentiment","Text Analysis on URL","About"] # Define the activities for the sidebar
#     choice = st.sidebar.selectbox("Choose Activity",activities) # Create a selectbox in the sidebar for activity selection
#     if choice == "Sentiment":
#         st.subheader("Sentiment Analysis") # Set the subheader for sentiment analysis
#         raw_text = st.text_area("Enter Text Here", "Type here...") # Create a text area for user input
#         if st.button("Analyze"): # Create an analyze button
#             blob = TextBlob(raw_text) # Create a TextBlob object from the input text
#             result_sentiment = blob.sentiment.polarity # Get the sentiment polarity
#             if result_sentiment > 0.0:
#                 custom_emoji = emoji.emojize(":smile:",language="alias") # Get the smile emoji 
#             elif result_sentiment < 0.0:
#                 custom_emoji = emoji.emojize(":disappointed:",language="alias") # Get the disappointed emoji
#             else:
#                 custom_emoji = emoji.emojize(":neutral_face:",language="alias") # Get the neutral face emoji
    
#     ## Choice is Text Analysis on url
#     elif choice == "Text Analysis on URL": 
#         st.subheader('Text Analysis from A Web URL')

#         raw_url = st.text_input("Enter a URL:")
#         text_preview_length = st.slider("Length to Preview",50,500)
#         if st.button('Submit'):
#             if raw_url: 
#                 result = get_text(raw_url)
#                 blob = TextBlob(result)
#                 len_of_full_text = len(result)
#                 len_of_short_text = round(len(result)/text_preview_length)
#                 ## Display the results
#                 st.success(f"Length of full text:{len_of_full_text}")
#                 st.success(f"length of short text:{len_of_short_text}")
#                 st.info(result[:len_of_short_text])

#                 c_sentences = [str(sent) for sent in blob.sentences] # Get the sentences from the TextBlob object
#                 c_sentiment = [sent.sentiment.polarity for sent in blob.sentences] # Get the sentiment polarity for each sentence

#                 new_df = pd.DataFrame(zip(c_sentences,c_sentiment),columns=["Sentences","Sentiment"]) # Create a DataFrame from the sentences and their corresponding sentiment polarity
#                 st.dataframe(new_df) # Display the DataFrame in the web app
    
#     ## Choice is about
#     else: 
#         st.subheader("About This App")
#         st.info("This is a sentiment analysis web app that has been made using NLP and ML. " \
#         "We return the sentiment, emoji of the given text. We also perform web scraping to understand and analyse text of websites."\
#         "This is an interactive app. Enjoy!!!"
#         )

# if __name__ == "__main__":
#     main()

import streamlit as st
from textblob import TextBlob
import pandas as pd
import emoji
from bs4 import BeautifulSoup
import requests

# Page config
st.set_page_config(page_title="Sentiment Analysis Web App", layout="centered")


# -------------------------------
# Fetch text from URL (Fixed 403)
# -------------------------------
@st.cache_data
def get_text(raw_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(raw_url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        fetched_text = " ".join([p.get_text() for p in paragraphs])

        return fetched_text

    except Exception as e:
        return None


# -------------------------------
# Main App
# -------------------------------
def main():
    st.title("🧠 Sentiment Analysis Web App using NLP and ML!")

    activities = ["Sentiment", "Text Analysis on URL", "About"]
    choice = st.sidebar.selectbox("Choose Activity", activities)

    # -------------------------------
    # SENTIMENT ANALYSIS
    # -------------------------------
    if choice == "Sentiment":
        st.subheader("🔍 Analyze Text Sentiment")

        raw_text = st.text_area("Enter Text Here", "Type here...")

        if st.button("Analyze",key="analyze_btn"):
            if raw_text.strip() == "":
                st.warning("Please enter some text!")
            else:
                blob = TextBlob(raw_text)
                polarity = blob.sentiment.polarity

                # Emoji mapping
                if polarity > 0:
                    mood = "Positive"
                    custom_emoji = emoji.emojize(":smile:", language="alias")
                elif polarity < 0:
                    mood = "Negative"
                    custom_emoji = emoji.emojize(":disappointed:", language="alias")
                else:
                    mood = "Neutral"
                    custom_emoji = emoji.emojize(":neutral_face:", language="alias")

                # Display results
                st.info(f"Sentiment: {mood} {custom_emoji}")
                st.success(f"Polarity Score: {polarity}")

    # -------------------------------
    # URL TEXT ANALYSIS
    # -------------------------------
    elif choice == "Text Analysis on URL":
        st.subheader("🌐 Analyze Text from Website")

        raw_url = st.text_input("Enter a URL:")
        text_preview_length = st.slider("Preview Length", 50, 500, 150)

        if st.button("Submit",key="submit_btn"):
            if not raw_url:
                st.warning("Please enter a URL!")
            else:
                result = get_text(raw_url)

                if not result:
                    st.error("Unable to fetch text. Website may block scraping.")
                else:
                    blob = TextBlob(result)

                    # Display basic stats
                    st.success(f"Total Length: {len(result)} characters")
                    st.write("### Preview:")
                    st.info(result[:text_preview_length])

                    # Sentence-wise sentiment
                    sentences = [str(sent) for sent in blob.sentences]
                    sentiments = [sent.sentiment.polarity for sent in blob.sentences]

                    df = pd.DataFrame({
                        "Sentence": sentences,
                        "Sentiment": sentiments
                    })

                    st.write("### Sentence Sentiment Analysis")
                    st.dataframe(df)

    # -------------------------------
    # ABOUT SECTION
    # -------------------------------
    else:
        st.subheader(" About This App")
        st.info(
            "This is a Sentiment Analysis web app built using NLP (TextBlob) and Streamlit. "
            "It analyzes text input and extracts sentiment polarity. "
            "It also supports website text scraping for analysis."
        )


# Run app
if __name__ == "__main__":
    main()

