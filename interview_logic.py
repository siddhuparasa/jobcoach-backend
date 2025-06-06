import os
import requests
from dotenv import load_dotenv

load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

def generate_feedback(role, answer):
    prompt = f"""
You are an interviewer for a {role} position.

Candidate's answer:
\"\"\"{answer}\"\"\"

Provide a very concise 1-line feedback summary, followed by clear improvement tips and an overall score out of 10.

Format your response exactly like this:

Feedback: <one line feedback summary>
Improvement Tips: <short bullet points or sentences>
Overall Score: <score out of 10>
"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
