from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import  RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

import streamlit as st

st.set_page_config(page_title="AI Text Assistant", page_icon="")

st.title('AI Chatbot')
st.write("This chatbot is created by Abhishek Joshi")
st.markdown("Hello! I'm Jarvis. How can I assist you today?")

def get_api_key():
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = ""
    api_key = st.text_input("Enter your Google API Key:", type = "password", key ="api_key")
    return api_key

api_key = get_api_key()

if not api_key:
    st.warning("Please enter your API Key to continue.")
else:

    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a helpful AI assistant. Please respond to user queries in English."
            ),
            MessagesPlaceholder(variable_name = "chat_history"),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )

    msgs = StreamlitChatMessageHistory(key = "langchain_messages")

    model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash" , google_api_key = api_key)

    chain = prompt | model | StrOutputParser()

    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: msgs,
        input_messages_key = "question",
        history_messages_key = "chat_history",
    )


    user_input = st.text_input("Enter your question in English:","")

    if user_input:
        st.chat_message("human").write(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            config = {"configurable": {"session_id":"amny"}}

            response = chain_with_history.stream({"question":user_input}, config)

            for res in response:
                full_response += res or ""
                message_placeholder.markdown(full_response + "|")
                message_placeholder.markdown(full_response)
    else:
        st.warning("Please enter your question")
        