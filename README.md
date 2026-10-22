# The Ordinary Museum

The Ordinary Museum is a web application that takes the user input of an everyday object and turns it into contemporary artworks. Users describe something ordinary, such as a water bottle, a hair tie or anything that comes to mind and the application uses the OpenAI API to generate a fictional museum wall label and an image of the object displayed in an exhibition.

![The Ordinary Museum app screenshot](static/everydayObject.png)

## Live app

[Open The Ordinary Museum](https://minimal-flask-app-cart498.onrender.com).

## Run locally

Run these commands from the repository root (the folder containing `app.py`). You need Python 3 with `pip` and `venv`, plus an OpenAI API key with access to the models used in `app.py`: `gpt-4.1` for labels and `gpt-image-1` for images. Submitting an object makes paid API requests and requires internet access.

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install flask openai python-dotenv
```

For a fresh checkout, copy the environment template:

```bash
cp .env-bup .env
```

If `.env` already exists, keep it and edit it instead of copying over it. Open `.env` in your editor and set:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Start the server:

```bash
python app.py
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install flask openai python-dotenv
```

For a fresh checkout, copy the environment template:

```powershell
Copy-Item .env-bup .env
```

If `.env` already exists, keep it and edit it instead. Set `OPENAI_API_KEY` as shown above, then start the server:

```powershell
python app.py
```

If `python` is not recognized, use `py` to create the environment (`py -m venv venv`). If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` in that terminal and retry. In Command Prompt, activate with `venv\Scripts\activate.bat`; in Git Bash on Windows, use `source venv/Scripts/activate`.

### Open and stop the app

Open **http://127.0.0.1:5000**. Enter an object description, such as “A blue reusable water bottle with scratches on the side,” and click **Enter the Exhibition**. The server generates the label first, then the exhibition image, so keep the page open while it works.

Press **Ctrl+C** in the terminal to stop the server. Run `deactivate` to leave the virtual environment. On later runs, activate the existing environment and run `python app.py`; you only need to install packages again if the environment is recreated or dependencies change.

`python app.py` enables Flask's debug mode for local development. For deployment, use the Gunicorn command below.

## Entry point and project structure

| File | Purpose |
| --- | --- |
| `app.py` | Entry point. Loads `.env`, creates the Flask application (`app`), and starts the local server when run directly. |
| `templates/index.html` | Jinja template for the object form, loading indicator, generated image, and wall label. |
| `static/styles.css` | Page styling and responsive exhibition layout. |
| `static/everydayObject.png` | Screenshot used in this README. |
| `.env-bup` | Environment template to copy to your local `.env`. |

`GET /` displays the form. `POST /` reads the `prompt` form field, calls the OpenAI API to generate a fictional label, then generates an image based on that label. The image is returned inline as base64 data. The app has no database or saved exhibition history.

There is currently no dependency manifest; install the three packages listed above. Gunicorn is an additional dependency for deployment on Linux.

## Troubleshooting

- **`ModuleNotFoundError`:** Activate `venv` and run `python -m pip install flask openai python-dotenv` in the same terminal used to start the app.
- **Missing key or authentication errors:** Set `OPENAI_API_KEY` in `.env` beside `app.py` and restart the server. `load_dotenv()` loads that file automatically. An existing terminal environment variable takes precedence over `.env`; check it if changing the file has no effect. Keep the key private; `.env` is ignored by Git.
- **Billing, rate limit, or model access errors:** Check the API account's billing, limits, and access to both models configured in `app.py`. The app displays API exceptions in the result area.
- **Port 5000 already in use:** Stop the other process, or run `python -m flask --app app run --debug --port 5001` and open http://127.0.0.1:5001.
- **VS Code environment injection warning:** Terminal injection is optional here because the app calls `load_dotenv()` itself.

## Deploy on Render

Configure a Python web service with these settings:

- **Build command:** `python -m pip install flask openai python-dotenv gunicorn`
- **Start command:** `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 240`
- **Environment variable:** Set `OPENAI_API_KEY` to your API key in the service configuration.

In `app:app`, the first `app` is the module `app.py` and the second is the Flask application object. The timeout allows more time for the sequential text and image requests. Gunicorn is for Linux deployment; it is not needed to run the app locally and does not run natively on Windows.

If deployment reports `gunicorn: command not found` or `No module named 'openai'`, check that the build command installs the corresponding package. If logs show `WORKER TIMEOUT`, check the API request duration and the configured timeout.

## International Art English (IAE) Features and Prompt Rules

I focused on the exaggerated language often used in contemporary art writing, as discussed by Alix Rule and David Levine in International Art English.

The main features were:

1. Abstract and theoretical language: Instead of explaining an object in simple terms, the AI uses concepts such as identity and materiality to give it a deeper meaning.
2. Unnecessarily complicated descriptions: The AI uses longer sentences and theoretical terminology to make ordinary objects seem of greater importance.
3. Treating everyday things as important artworks: The language gives objects an exaggerated sense of cultural and artistic importance.

I translated these features into explicit rules in my developer prompt. The AI is instructed to use exaggerated International Art English, describe the original object accurately, and treat it as an important piece of contemporary art.

## Reflection

I think a language model is so fluent in International Art English because this type of writing follows recognizable patterns. Even when the language sounds complex, it often repeats similar structures and finds easy ways of connecting ideas.

Language models learn from large amounts of text, so they become good at recognizing and reproducing these patterns. They don't necessarily need to understand the artistic importance of an object to generate a convincing interpretation of it.

This also made me question how much of the meaning we associate with art comes from the object itself and how much comes from the context surrounding it. It doesn't matter what you're presenting, as long as you find a way to give it the importance and the right meaning, it will look more relevant/important to people.

I think the AI's ability to imitate this way of writing is both funny and interesting because it shows how artistic language can sometimes become predictable, even when it is trying to sound original.

## User guide

Using The Ordinary Museum is simple:

Open the web application.

Enter a description of an everyday object into the text field. For example, "A blue reusable water bottle with scratches on the side."

Click Enter the Exhibition.

The application generates a fictional museum wall label and an image of the object displayed as contemporary art.

View the artwork and its interpretation together, with the image on the left and the wall label on the right.

Enter another object to create a new exhibition.

The application uses Flask for the website, HTML and CSS for the layout, and the OpenAI API for generating the text and image.

Because both the label and image are generated using AI, the results may vary each time, even when the same object is submitted.
