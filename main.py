import streamlit as st
from services.openai_service import get_openai_response, get_user_prompt_type

# Frontend
st.title("ChatGPT-like clone")


# Initialize OpenAI model in session state if not already present
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize the messages in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ask for username (or you can use any authentication method)
username = st.text_input("Enter your username", key="username")

# Only proceed after the user has entered a username
if username:        

    # Get prompt type based on username and extend messages if first interaction
    if not st.session_state.messages:
        initial_prompts = get_user_prompt_type(username)
        st.session_state.messages.extend(initial_prompts)

    # Display previous messages in the chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input(f"Bonjour?"):
        # Append user input to messages
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in the chat
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call OpenAI API (logic handled in services)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_openai_response(st.session_state["openai_model"], st.session_state.messages)

            # Display the response
            message_placeholder.markdown(full_response)

        # Append assistant's response to messages
        st.session_state.messages.append({"role": "assistant", "content": full_response})
