import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from modules.agent import handle_user_input

st.title("AI Executive Admin")

user_input = st.text_area("Enter your request:")

if st.button("Submit"):
    if user_input.strip():
        response = handle_user_input(user_input)
        st.markdown(f"**Assistant:** {response}")
    else:
        st.warning("Please enter a request.") 