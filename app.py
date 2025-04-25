from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# ✅ Your Hugging Face API key
HF_API_KEY = "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"
# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def ask_mistral(prompt):
    payload = {
        "inputs": f"You:- {prompt} \n Bot:-",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        else:
            return "Sorry, I didn't understand the response."
    else:
        return f"Error: {response.status_code}\n{response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["question"]
        response = ask_mistral(user_input)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
