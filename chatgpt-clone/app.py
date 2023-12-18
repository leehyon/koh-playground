"""
File: app.py
Description: This is the main file for the Flask web application used to build a ChatGPT clone.
Author: Leehyon Koh
Copyright: Kohsruhe 2023
Last updated: 2023-12-15
"""

# Import Flask and OpenAI 
from flask import Flask, request, render_template
from openai import OpenAI  
# import config
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model parameters 
MAX_TOKENS = 1024
TEMPERATURE = 0.5 

# Chat history to provide conversation context for OpenAI
chat_history = []

# Initialize API client
# openai = OpenAI(api_key=config.OPENAI_API_KEY)
# openai will automatically look for an environment variable named OPENAI_API_KEY.
openai = OpenAI()

@app.route("/")
def index():
    # Render homepage template
    return render_template("index.html")
    
    
@app.route("/get") 
def get_bot_response():
    try: 
        user_text = request.args.get('msg') 

        # Append user message to chat history   
        chat_history.append({"role": "user", "content": user_text})

        # Pass chat history to OpenAI for response
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        if response.usage.total_tokens >= MAX_TOKENS:
            logger.warning("OpenAI API token usage exceeded!")
            # Clear chat history if token limit reached
            chat_history.clear() 
            return "Max tokens reached, clearing chat history"

        # Extract bot's response and append to chat log 
        bot_response = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_response})

        return bot_response
    
    except Exception as exc:
        logger.exception("Error processing request: %s", exc)
        return "Oops, something went wrong!"

    
if __name__ == "__main__":
    # Run app in debug mode
    app.run(debug=True)