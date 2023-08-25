import os
from llama_index import download_loader, VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import streamlit as st
import openai

# Configuration
st.set_page_config(page_title="Chat with the Streamlit docs, powered by LlamaIndex", 
                   page_icon="🦙", layout="centered", 
                   initial_sidebar_state="auto")

openai.api_key = st.secrets["openai_key"]

# Display
st.title("Chat with the Streamlit docs, powered by LlamaIndex 💬🦙")
st.info("Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}]

@st.cache(show_spinner=False, suppress_st_warning=True)
def load_data():
    ChatGPTRetrievalPluginReader = download_loader("ChatGPTRetrievalPluginReader")
    bearer_token = st.secrets["BEARER_TOKEN"]

    reader = ChatGPTRetrievalPluginReader(
        endpoint_url="YOUR_PUBLIC_ENDPOINT",  # Replace with your deployed endpoint
        bearer_token=bearer_token
    )

    docs = reader.load_data("text query")
    
    service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features."))
    
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    return index

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
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
