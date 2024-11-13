import os

import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import constants
from prompts import Prompt
os.environ["GOOGLE_API_KEY"] = constants.gkey
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0)  # Replace with actual model and key


def call_gemini(prompt):
  msg = model.predict(prompt)
  return "LLM response for prompt: {}".format(msg)

def main():
  # Title and description
  st.title("AI Travel Advisor ")
  st.subheader("Personalized travel suggestions based on your preferences.")

  # Text input fields with placeholders for better guidance
  origin = st.text_input("Enter Origin City or Country:")
  destination = st.text_input("Enter Destination City or Country:")

  if origin and destination:
    selected_preference=st.selectbox("Travel Preference",
                 ["Faster Travel Time", "Cheaper Option", "Scenic Route", "Balanced (Time & Cost)","Alternate route options"]),

    if "selected_preference" not in st.session_state:
        # print("initializing session var 'selected_number'")
        st.session_state["selected_preference"] = "Faster Travel Time"




    p= Prompt()
    prompts = p.get_travel_prompts(origin,destination,selected_preference)
    travel_suggestions = call_gemini(prompts)
    st.write("**Travel Suggestions:**")
    if travel_suggestions:
      st.success(travel_suggestions)  # Use success message for positive outcome
    else:
      st.error("We couldn't find suggestions for your criteria yet. Try adjusting your preferences.")


# call the function
main()
