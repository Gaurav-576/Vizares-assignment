# Conversational Bot

**Conversational Bot** is an AI-driven chatbot application built using **DialoGPT** for generating human-like responses. 
Additionally, it provides real-time **weather** and **time** functionalities. The chatbot is integrated with **Streamlit** for an interactive web interface.

---

## 🌐 Explore the Chatbot Live

Check out the live version of the chatbot (Streamlit deployment):  
👉 **[Conversational Bot Live Website](https://link_to_your_live_site)**

Interact with the chatbot for weather updates, time, and natural language conversations!

---

## 🖼️ Conversational Bot in Action

### User Interface
![Chatbot Interface](./images/interface.png)

### Example Interaction - Time Query
![Chatbot Interaction](./images/time.png)

### Example Interaction - Weather Query
![Chatbot Interaction](./images/weather.png)

*(Add screenshots showing the chatbot's functionality here)*

---

## 🌟 **Key Features**

1. **AI-Powered Conversations:**
   - Uses **DialoGPT** for natural language responses.
   - Provides interactive chatbot functionality.

2. **Weather Information:**
   - Fetches real-time weather data using a **weather API**.

3. **Time Queries:**
   - Retrieves the current time dynamically.

4. **User-Friendly Interface:**
   - Built using **Streamlit** for easy interaction.

5. **Secure API Key Management:**
   - Uses **st.secrets** for handling API keys securely.

---

## 🛠 **Project Structure**

```plaintext
Conversational-Bot/
├── app.py                    # Main chatbot application
├── requirements.txt          # Python dependencies
├── .streamlit/secrets.toml   # Secure API key storage
├── README.md                 # Project documentation
```

---

## 🚀 **How It Works**

1. **User enters a query** (e.g., "What's the weather in Kolkata?" or "What time is it?").  
2. **Bot processes the query:**  
   - If it's a weather-related query, it fetches data from the **weather API**.
   - If it's a time-related query, it retrieves the current time.
   - Otherwise, it responds with **DialoGPT-generated replies**.  
3. **Response is displayed** in the chatbot interface.  

---

## 💻 **Installation and Setup**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/conversational-bot.git
   cd conversational-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Keys**:  
   - Create a `.streamlit/secrets.toml` file and add your **Weather API Key**:
     ```toml
     [secrets]
     WEATHER_API_KEY = "your_weather_api_key_here"
     ```

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

---

## 📜 **License**

This project is licensed under the [MIT License](LICENSE).

---

## ✍️ **Creator**

Developed by **Gaurav Kumar Singh**  
👔 [LinkedIn](https://www.linkedin.com/in/gaurav-singh-mlops/) | 📦 [GitHub](https://github.com/Gaurav-576)

---
