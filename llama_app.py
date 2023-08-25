import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
from openai.error import OpenAIError  # To catch specific OpenAI errors
import tenacity  # Import the tenacity library for its RetryError

st.set_page_config(page_title="Geoff's attempt at a Llama chat app", ...)

openai.api_key = st.secrets["openai_key"]
st.title("Chat with the Streamlit docs, powered by LlamaIndex 💬🦙")
st.info("Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}
    ]

@st.cache_resource(show_spinner=False, ttl=3600)  # Cache for an hour
@tenacity.retry(wait=tenacity.wait_fixed(60), stop=tenacity.stop_after_attempt(3), reraise=True)
def load_data():
    try:
        with st.spinner(text="Loading and indexing the Streamlit docs..."):
            reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
            docs = reader.load_data()
            service_context = ServiceContext.from_defaults(
                llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, ...))
            index = VectorStoreIndex.from_documents(docs, service_context=service_context)
            return index
    except openai.error.RateLimitError:
        st.error("We've hit the OpenAI API rate limit. Please try again later.")
        return None

index = load_data()
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
            except tenacity.RetryError as e:
                # Check if the underlying exception is a RateLimitError
                if "RateLimitError" in str(e.last_attempt.exception()):
                    st.write("Sorry, I'm getting too many requests right now. Please wait a moment and try again.")
                else:
                    st.write("Sorry, there was an error processing your request.")
            except Exception as e:  # Catch any other general exceptions
                st.write(f"An unexpected error occurred: {e}")

