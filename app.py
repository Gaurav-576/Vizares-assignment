import streamlit as st
from utility import model
chatbot = model.ChatBot()

st.set_page_config(page_title="Conversational AI ChatBot 🤖", page_icon=":robot:", layout="centered")

st.title("🤖 Conversational AI ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello, how can I help you today?"})

with st.sidebar:
    st.title("Vizares Conversational AI ChatBot")
    st.write("Powered by **DialoGPT** and **Streamlit**")
    st.markdown(
        """
        ### Made by
        **Gaurav Kumar Singh**
        
        - **GitHub**: [Gaurav-576](https://github.com/Gaurav-576)
        - **LinkedIn**: [Gaurav Singh](https://www.linkedin.com/in/gaurav-singh-mlops)
        - **Resume**: [View Resume](https://drive.google.com/file/d/1wwiiCCLx70kJSNuj1i497t3A4G72m0g4/view?usp=drive_link)
        
        ### About the Project:
        This conversational chatbot is built using **DialoGPT** as the core model, integrated with **Streamlit** for an interactive user interface.
        """
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Enter message here...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Chatbot is thinking..."):
        bot_response = chatbot.get_response(user_input)
        st.chat_message("assistant").markdown(bot_response)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

st.markdown("""
    <style>
        .css-1v3fvcr {display: none;}
        .css-ffhzg2 {padding-top: 1rem; padding-bottom: 1rem;}
        .streamlit-expanderHeader {font-size: 24px;}
        .streamlit-expanderContent {padding: 1rem;}
    </style>
""", unsafe_allow_html=True)
