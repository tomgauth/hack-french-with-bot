from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

st.session_state["openai_model"] = "gpt-3.5-turbo"

# Function to get OpenAI API response
def get_openai_response(model, messages):

    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )
    response = st.write_stream(stream)

    # Collect the full response as a string
    full_response = ""
    for chunk in stream:
        chunk_message = chunk['choices'][0]['delta'].get('content', '')
        full_response += chunk_message
    
    return full_response

# Function to get prompt type based on username
def get_user_prompt_type(username):
    """
    Returns a role-playing prompt structure based on the username.
    
    :param username: The username of the user.
    :return: A list of dicts defining the role and content for the role-play prompt.
    """
    if username == "tomg":
        # Role-playing scenario for practicing French conversation with a busy boulangère
        return [
            {"role": "system", "content": "You are playing the role of a busy Parisian boulangère. You are focused on quickly selling items and moving on to the next customer. You only speak French."},
            {"role": "user", "content": """You are interacting with a customer. Your goal is to sell your products, not engage in small talk. You should be direct, efficient, and polite, but not overly helpful. Here's the context for the conversation."""}
        ]
    else:
        # General conversation prompt
        return [
            {"role": "system", "content": "You are a helpful assistant in a general conversation."},
            {"role": "user", "content": "Let's have a general conversation. Feel free to ask me any questions to continue."}
        ]
