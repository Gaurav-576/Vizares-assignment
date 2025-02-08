import os
import requests
import streamlit as st
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
from datetime import datetime

load_dotenv()

class ChatBot:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.weather_api_key = st.secrets["WEATHER_API_KEY"]

    def get_response(self, user_input):
        if "weather" in user_input.lower() or "temperature" in user_input.lower():
            return self.get_weather()
        elif "time" in user_input.lower() or "current time" in user_input.lower():
            return self.get_time()
        else:
            new_user_input = self.tokenizer(user_input + self.tokenizer.eos_token, return_tensors='pt', padding=True, truncation=True)
            new_user_input_ids = new_user_input["input_ids"]
            attention_mask = new_user_input["attention_mask"]
            
            chat_history_ids = self.model.generate(
                new_user_input_ids, 
                attention_mask=attention_mask,  
                max_length=1000,
                pad_token_id=self.tokenizer.eos_token_id
            )

            response = self.tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)
            
            if response == "" or "i am" in response.lower():
                response = "I'm sorry, I didn't understand that. Could you please rephrase?"
            
            return response

    def get_weather(self):
        url = f"http://api.weatherstack.com/current?access_key={self.weather_api_key}&query=Kolkata"
        response = requests.get(url)
        data = response.json()
        
        if "current" in data:
            temp = data["current"]["temperature"]
            weather_desc = data["current"]["weather_descriptions"][0]
            return f"The current temperature in Kolkata is {temp}°C with {weather_desc}."
        else:
            return "Sorry, I couldn't fetch the weather details right now."

    def get_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."


st.set_page_config(page_title="Conversational AI ChatBot 🤖", page_icon=":robot:", layout="centered")
st.title("🤖 Conversational AI ChatBot")

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

chatbot = ChatBot()
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello, how can I help you today?"})

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
