import openai
import streamlit as st

# Page configuration.
st.set_page_config(
    page_title="Chat with the Streamlit docs, powered by OpenAI",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Set the OpenAI API key.
openai.api_key = st.secrets["openai_key"]

# Display title and info.
st.title("💬 Chatbot")
st.write("Welcome to the futuristic chatbot! How can I assist you today?")

# Initialize session state for messages if not already done.
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages.
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# When the user submits a new question or statement.
if prompt := st.chat_input():
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages + [{"role": "user", "content": prompt}])
        msg = response.choices[0].message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg.content)
    except openai.error.RateLimitError:
        st.warning("Sorry, we have reached the maximum number of requests for now. Please try again later.")
