import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
from openai.error import OpenAIError
import tenacity

# Page configuration.
st.set_page_config(
    page_title="Chat with the Streamlit docs, powered by LlamaIndex",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Set the OpenAI API key.
openai.api_key = st.secrets["openai_key"]

# Display title and info.
st.title("Chat with the Streamlit docs, powered by LlamaIndex 💬🦙")
st.info(
    "Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)",
    icon="📃"
)

# Initialize session state for messages if it doesn't exist.
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about Streamlit's open-source Python library!"
        }
    ]

# Cached data loader with adjusted retry mechanism for GPT Premium's higher rate limits.
@st.cache_resource(show_spinner=False, ttl=3600)
@tenacity.retry(wait=tenacity.wait_fixed(30), stop=tenacity.stop_after_attempt(5), reraise=True) # Reduced wait time due to higher rate limits for premium users.
def load_data():
    try:
        with st.spinner(text="Loading and indexing the Streamlit docs..."):
            reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
            docs = reader.load_data()
            service_context = ServiceContext.from_defaults(
                llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="... (rest of your prompt)")
            )
            index = VectorStoreIndex.from_documents(docs, service_context=service_context)
            return index
    except openai.error.RateLimitError:
        st.error("We've hit the OpenAI API rate limit. Please try again in a bit.")
        return None

index = load_data()

# Proceed if index is loaded.
if index:
    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

    # Get user input.
    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    # Display the chat history.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Respond to the user's message if it's the latest.
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."): # Since premium provides faster response times, the user experience will be smoother.
                try:
                    response = chat_engine.chat(prompt)
                    st.write(response.response)
                    message = {"role": "assistant", "content": response.response}
                    st.session_state.messages.append(message)
                except tenacity.RetryError as e:
                    if "RateLimitError" in str(e.last_attempt.exception()):
                        st.write("Sorry, I'm getting too many requests right now. Please wait a bit and try again.")
                    else:
                        st.write("Sorry, there was an error processing your request.")
                except Exception as e:
                    st.write(f"An unexpected error occurred: {e}")

