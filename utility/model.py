import os
import requests
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
from datetime import datetime

# Load environment variables
load_dotenv()

class ChatBot:
    def __init__(self):
        # Initialize DialoGPT model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Get weather API key from environment variable
        self.weather_api_key = os.getenv("WEATHER_API_KEY")

    def get_response(self, user_input):
        # Check if the user input contains requests for weather or time
        if "weather" in user_input.lower() or "temperature" in user_input.lower():
            return self.get_weather()
        elif "time" in user_input.lower() or "current time" in user_input.lower():
            return self.get_time()
        else:
            # If it's a general query, use DialoGPT for response
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
            
            # Fallback response if no useful reply is generated
            if response == "" or "i am" in response.lower():
                response = "I'm sorry, I didn't understand that. Could you please rephrase?"
            
            return response

    def get_weather(self):
        # Fetch weather data using the weather API
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
        # Fetch the current time using the datetime library
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."
