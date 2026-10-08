from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image = None

    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            response = openai.responses.create(
                model="gpt-4.1",  
                input=[{"role": "developer", "content": "You are a helpful assistant that provides concise and accurate answers to user queries."}, 
                          {"role": "user", "content": prompt}],
                          temperature=1.2,
                          max_output_tokens=50
            )
            result = response.output_text

            image_response = openai.images.generate(
                model="gpt-image-1",
                prompt=result,
                size="1024x1024"
            )

            image = image_response.data[0].b64_json

        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result, image=image)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing