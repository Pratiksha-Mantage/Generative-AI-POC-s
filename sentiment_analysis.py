from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import constants
os.environ["GOOGLE_API_KEY"]= constants.gkey
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0)
def get_sentiment(user_input):
    prompt = f""" You are a helpful AI sentiment analyzer .\n
    Please provide me the sentiment analysis of below text.\n
    text:{user_input}"""

    sentiment = model.predict(prompt)
    return sentiment


#Configures the default settings of the page.
st.set_page_config(page_title="Sentiment")
st.header("Sentiment Analyzer Application")
user_input = st.text_input("Input: ", key="input")
if user_input:
    submit = st.button("Enter")
    if submit:
        sentiment = get_sentiment(user_input)
        st.subheader("Sentiment analysis of above text")
        st.write(sentiment)
else:
    st.warning("Please enter input text")
