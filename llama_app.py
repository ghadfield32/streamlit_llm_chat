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
st.image("path_to_robot_image.jpg", use_column_width=True)  # Assuming you've added an image of the robot
st.write("Welcome to the futuristic I, Robot themed chatbot! How can I assist you today?")

# Initialize session state for messages if not already done.
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Initialize the API call counter if it doesn't exist
MAX_PROMPTS = 10  # adjust according to your needs
if "api_calls" not in st.session_state:
    st.session_state["api_calls"] = 0

# Display previous messages.
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# When the user submits a new question or statement.
if prompt := st.chat_input():
    if st.session_state["api_calls"] < MAX_PROMPTS:
        # Make the API call
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg.content)

        # Increment the counter
        st.session_state["api_calls"] += 1
    else:
        st.warning("Sorry, we have reached the maximum number of requests for now. Please try again later.")
