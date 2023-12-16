"""
File: app.py
Description: Main file for the Flask app that provides AI-powered code fixing.
Author: Leehyon Koh
Copyright: Kohsruhe 2023
Last modified: 2023-12-16
"""

from flask import Flask, render_template, request
from openai import OpenAI
import config

app = Flask(__name__)

# Constants for OpenAI requests
MAX_TOKENS = 1024
TEMPERATURE = 0.5 

# Initialize OpenAI client
openai = OpenAI(api_key=config.OPENAI_API_KEY)

@app.route("/", methods=["GET", "POST"])
def index():
    """Route to show the main page and handle code fixing requests"""

    if request.method == "POST":

        # Get posted code and error  
        code = request.form["code"]
        error = request.form["error"]

        # Request explanation from OpenAI
        explanation_prompt = (f"Explain the error in this code without fixing it:"
                  f"\n\n{code}\n\nError:\n\n{error}")
        explanation = get_openai_response(explanation_prompt)

        # Request fixed code from OpenAI 
        fixed_code_prompt = (f"Fix this code: \n\n{code}\n\nError:\n\n{error}."
                             f" \n Respond only with the fixed code.")
        fixed_code = get_openai_response(fixed_code_prompt)
        
        # Render page with explanations and fixed code
        return render_template("index.html", explanation=explanation, fixed_code=fixed_code)
    
    # Handle GET request - render main page
    else:
        return render_template("index.html")
    

def get_openai_response(prompt):
    """Request response from OpenAI"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # Run debug server
    app.run(debug=True)

