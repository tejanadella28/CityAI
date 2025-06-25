from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from dotenv import load_dotenv
from analysis.sentiment import analyze_sentiment
import json
import requests
from datetime import datetime

# ==================================================
# ⚡️ Load Environment
# ==================================================
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
device = "cuda" if torch.cuda.is_available() else "cpu"

# ==================================================
# ⚡️ Model Configuration
# ==================================================
IBM_MODEL_NAME = "ibm-granite/granite-3.3-2b-instruct"

if device == "cuda":
    ibm_tokenizer = AutoTokenizer.from_pretrained(IBM_MODEL_NAME, use_auth_token=HF_TOKEN)
    ibm_model = AutoModelForCausalLM.from_pretrained(
        IBM_MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto",
        use_auth_token=HF_TOKEN
    )
else:
    ibm_tokenizer, ibm_model = None, None

app = Flask(__name__)

# ==================================================
# ⚡️ Routes
# ==================================================
@app.route("/")
def index():
    return jsonify({"message": "Citizen AI API is running"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_query = data.get("query", "").strip()
        if not user_query:
            return jsonify({"error": "Query is required"}), 400

        if device == "cuda":
            reply = call_ibm_model(user_query)
        else:
            reply = call_groq_model(user_query)

        sentiment = analyze_sentiment(user_query)
        save_interaction(user_query, reply, sentiment)

        return jsonify({"reply": reply, "sentiment": sentiment})
    except Exception as e:
        print(f"[Server Error] {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Return all feedback entries as JSON for Streamlit."""
    data_file = "data/feedback.json"
    feedback = []
    if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
        with open(data_file, "r") as f:
            feedback = json.load(f)
    return jsonify(feedback)

# ==================================================
# ⚡️ Model Call Definitions
# ==================================================
def call_ibm_model(user_query):
    prompt = f"<|user|>\n{user_query}\n<|assistant|>\n"
    inputs = ibm_tokenizer(prompt, return_tensors="pt").to(ibm_model.device)

    with torch.no_grad():
        outputs = ibm_model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.5,
            top_p=0.9,
            do_sample=True,
            pad_token_id=ibm_tokenizer.eos_token_id
        )
    reply = ibm_tokenizer.decode(outputs[0], skip_special_tokens=True).split("<|assistant|>")[-1].strip()
    return reply

def call_groq_model(user_query):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": user_query}],
        "max_tokens": 100,
        "temperature": 0.5,
        "top_p": 1.0
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        print(f"[Groq API Error]: {e}")
        return "⚠️ Groq API error: Unable to connect or fetch response. Please try again later."

# ==================================================
# ⚡️ Save Interaction
# ==================================================
def save_interaction(user_query, reply, sentiment):
    """Save interaction to feedback.json with timestamp."""
    data_file = "data/feedback.json"
    entry = {
        "user_query": user_query,
        "reply": reply,
        "sentiment": sentiment,
        "timestamp": datetime.now().isoformat()
    }

    if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
        with open(data_file, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    os.makedirs("data", exist_ok=True)
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)

# ==================================================
# ⚡️ Main
# ==================================================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
