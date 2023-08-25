import openai
import streamlit as st

# Page configuration.
st.set_page_config(
    page_title="Chat with the Streamlit Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Set the OpenAI API key.
openai.api_key = st.secrets["openai_key"]

# Display robot image.
st.image("https://YOUR_IMAGE_URL_HERE.png", width=150, use_column_width=False)  # Replace with the URL to your robot image.

# Display title and info with creative styling.
st.title("💬 Chatbot")
st.markdown(
    """
    Welcome to the Streamlit Chatbot! 🤖
    
    Ask anything you'd like, and let the chatbot amaze you with its answers.
    """,
    unsafe_allow_html=True
)

# Initialize messages if they don't exist in the session state.
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]

# Display chat messages.
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"👤: {msg['content']}", unsafe_allow_html=True)
    else:
        st.markdown(f"🤖: {msg['content']}", unsafe_allow_html=True)

# Get user input and display the chatbot's response.
if prompt := st.text_input("Your Question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
