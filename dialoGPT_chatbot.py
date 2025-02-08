import os
import time
import torch
import datetime
import requests
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
tokenizer.pad_token = tokenizer.eos_token

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

class ChatBot:
    def __init__(self):
        self.chat_history_ids = None
        self.bot_input_ids = None
        self.end_chat = False
        self.welcome()

    def welcome(self):
        print("Initializing ChatBot ...")
        time.sleep(1)
        print('Type "quit" or "exit" to end chat \n')
        time.sleep(1)
        print("ChatBot >>  Hello! How can I help you today?")

    def user_input(self):
        text = input("User >> ").strip().lower()

        if text in ['bye', 'quit', 'exit']:
            self.end_chat = True
            print('ChatBot >>  See you soon! Bye!')
            time.sleep(1)
            print('\nQuitting ChatBot ...')
            return

        elif "time" in text:
            print(f'ChatBot >>  The current time is {datetime.datetime.now().strftime("%H:%M:%S")}')
            return

        elif "date" in text:
            print(f'ChatBot >>  Today\'s date is {datetime.datetime.now().strftime("%Y-%m-%d")}')
            return

        elif "weather" in text or "temperature" in text:
            self.get_weather()
            return

        elif "forecast" in text:
            self.get_weather_forecast()
            return

        self.new_user_input = tokenizer(
            text + tokenizer.eos_token, return_tensors='pt', 
            padding=True, truncation=True
        )
        self.new_user_input_ids = self.new_user_input["input_ids"]
        self.attention_mask = self.new_user_input["attention_mask"]

    def get_weather(self):
        print("ChatBot >> Fetching current weather details for Kolkata...")
        url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query=Kolkata"
        try:
            response = requests.get(url)
            data = response.json()
            if "current" in data:
                temp = data["current"]["temperature"]
                weather_desc = data["current"]["weather_descriptions"][0]
                print(f'ChatBot >> The current temperature in Kolkata is {temp}°C with {weather_desc}.')
            else:
                print("ChatBot >> Unable to fetch weather details.")
        except Exception as e:
            print("ChatBot >> Error fetching weather data.")

    def get_weather_forecast(self):
        """Fetches weather forecast for the next few days for Kolkata."""
        print("ChatBot >> Fetching weather forecast for Kolkata...")
        url = f"http://api.weatherstack.com/forecast?access_key={API_KEY}&query=Kolkata"
        try:
            response = requests.get(url)
            data = response.json()
            if "forecast" in data:
                forecast_data = data["forecast"]
                print(f"ChatBot >> Weather forecast for the next few days in Kolkata:")

                for date, forecast in forecast_data.items():
                    temp_max = forecast["maxtemp"]
                    temp_min = forecast["mintemp"]
                    weather_desc = forecast["hourly"][0]["weather_descriptions"][0]  # Taking the description of the first hour
                    print(f"Date: {date} | Max Temp: {temp_max}°C | Min Temp: {temp_min}°C | Weather: {weather_desc}")
            else:
                print("ChatBot >> Unable to fetch forecast details.")
        except Exception as e:
            print("ChatBot >> Error fetching forecast data.")

    def bot_response(self):
        if not hasattr(self, "new_user_input_ids"):
            return

        self.chat_history_ids = None  
        if self.chat_history_ids is not None:
            self.bot_input_ids = torch.cat([self.chat_history_ids, self.new_user_input_ids], dim=-1)
        else:
            self.bot_input_ids = self.new_user_input_ids

        self.chat_history_ids = model.generate(
            self.bot_input_ids, 
            attention_mask=self.attention_mask,  
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id
        )

        response = tokenizer.decode(self.chat_history_ids[:, self.bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        if response == "" or "i am" in response.lower():
            response = "I'm sorry, I didn't understand that. Could you please rephrase?"

        print('ChatBot >>  ' + response)

    def random_response(self):
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

bot = ChatBot()

while not bot.end_chat:
    bot.user_input()
    if not bot.end_chat:
        bot.bot_response()
