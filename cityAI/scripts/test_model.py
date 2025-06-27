import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = "ibm-granite/granite-3.3-2b-instruct"

# Load Model and Tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
    use_auth_token=HF_TOKEN
)

# Test
user_query = "Where can I get a birth certificate in Chennai?"
inputs = tokenizer(user_query, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.7,
        do_sample=True,
        top_p=0.9,
    )
reply = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("\nResponse:\n", reply)
