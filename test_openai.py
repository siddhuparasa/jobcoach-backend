import requests

url = "http://localhost:5000/ask"
payload = {
    "role": "ML Engineer",
    "answer": "I would use logistic regression for binary classification."
}

response = requests.post(url, json=payload)
print("Response from backend:")
print(response.json())
