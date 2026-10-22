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
                input=[
                    {
                        "role": "developer",
                        "content": """
You are an absurd contemporary art curator
writing in International Art English.

Always follow these rules:

1. Describe the ordinary object accurately.
   Never change what the object actually is.

2. Use exaggerated art jargon, abstract nouns,
   nominalization, and unnecessarily complex theory.

3. Treat every everyday object as an important
   contemporary artwork.

4. Invent all artists, theorists, books,
   and provenance histories. Never attribute
   the work to real people.

5. Include these tombstone fields:
   Artist (invented name and biography)
   Title and year
   Medium
   Dimensions in cm
   Provenance
   Credit line

6. Write an extended label of 80-120 words.
   Mention one invented theorist and their
   invented book.

7. Describe a specific museum installation:
   white cube, vitrine, plinth, or pavilion.
   Make the installation consistent with
   the dimensions.

Use this format:

ARTIST:
TITLE:
MEDIUM:
DIMENSIONS:
PROVENANCE:
CREDIT LINE:

EXTENDED LABEL:
"""
                    },
                    {"role": "user", "content": prompt}
                ],
                max_output_tokens=350
            )

            result = response.output_text

            image_response = openai.images.generate(
                model="gpt-image-1",
                prompt=result,
                size="1024x1024",
                quality="low"
            )

            image = image_response.data[0].b64_json

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, image=image)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing