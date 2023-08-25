import openai
import streamlit as st

# Page configuration.
st.set_page_config(
    page_title="🏀 Chat with a Basketball Pro!",
    page_icon="🏀",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Set the OpenAI API key.
openai.api_key = st.secrets["openai_key"]

# Display title and basketball-themed info.
st.title("🏀 Chat with a Basketball Pro!")
st.image("https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.si.com%2F.image%2Far_1%3A1%252Cc_fill%252Ccs_srgb%252Cfl_progressive%252Cq_auto%3Agood%252Cw_1200%2FMTY4MTkwMDY2NzYwNDkyOTU3%2F130528114807-jerry-west-01168771-nba-logo-single-image-cutjpg.jpg&tbnid=S6xMaH47oFDYrM&vet=12ahUKEwiymZ_gsviAAxVbvoQIHY2IDFMQMygAegQIARBN..i&imgrefurl=https%3A%2F%2Fwww.si.com%2Fnba%2F2014%2F05%2F28%2Fclassic-si-photos-jerry-west&docid=aRKeb2Nm8aJkuM&w=1200&h=1200&q=jerry%20west%20google%20images&client=firefox-b-1-d&ved=2ahUKEwiymZ_gsviAAxVbvoQIHY2IDFMQMygAegQIARBN", use_column_width=True)  # Change the URL to your preferred basketball image
st.write("Hey there! I've played and studied basketball for years. Ask me anything about the game, strategies, or stats!")

# Initialize session state for messages if not already done.
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages.
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# When the user submits a new question or statement.
if prompt := st.chat_input():
    try:
        # Adding context to make the model's response more basketball-centric
        context = "You are a professional basketball player with vast knowledge of the game's history, statistics, and strategies."
        full_prompt = f"{context}\n\nUser: {prompt}\nBasketball Pro:"
        
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", prompt=full_prompt, max_tokens=150)
        
        response_text = response.choices[0].text.strip()
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.chat_message("assistant").write(response_text)
    except openai.error.RateLimitError:
        st.warning("Sorry, we've dribbled too much and need a timeout. Please try again later!")
