import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain_openai import AzureChatOpenAI
from langchain.schema import(
    SystemMessage, 
    HumanMessage,
    AIMessage
)


def init():
    load_dotenv()

    if os.getenv("AZURE_OPENAI_API_KEY") is None or os.getenv("AZURE_OPENAI_API_KEY") == "":
        print("AZURE_OPENAI_API_KEY is not set")
        exit(1)
    else: 
        print("AZURE_OPENAI_API_KEY is set")

    if os.getenv("AZURE_OPENAI_ENDPOINT") is None or os.getenv("AZURE_OPENAI_ENDPOINT") == "":
        print("AZURE_OPENAI_ENDPOINT is not set")
        exit(1)
    else: 
        print("AZURE_OPENAI_ENDPOINT is set")

def main():

    init()

    chat = AzureChatOpenAI(
        azure_deployment="gpt4o",
        api_version="2024-08-01-preview",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )
    if "messages" not in st.session_state:

        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant."),
            #HumanMessage(content=input)
        ]


    st.set_page_config(page_title="ChatGPT", page_icon="🤖")
    st.header("Chatgpt 🤖")

    # message("Hello how are you?")
    # message("Fine thank you, how are you?", is_user=True)

    with st.sidebar:
        user_input = st.text_input("Your message:", key="user_input", placeholder="Type your message")


        if user_input:
            #message(user_input, is_user=True) #show the message
            st.session_state.messages.append(HumanMessage(content=user_input)) #append the user message to the collection
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages) #send the input to the model.
            st.session_state.messages.append(AIMessage(content=response.content))
            #message(response.content, is_user=False)

    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')

if __name__ == "__main__":
    main()
