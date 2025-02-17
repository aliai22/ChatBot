import os
import torch
import asyncio
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "./local_llm/"
model_id = "microsoft/phi-2"
model = None
tokenizer = None

async def load_model():
    global model, tokenizer
    if os.path.exists(model_path):
        print("Loading Phi-2 model from local directory...")
        model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype="auto")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
    else:
        print("Downloading Phi-2 model from Hugging Face...")
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype="auto",
            trust_remote_code=True
        )
        tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        
        # Save the model and tokenizer locally after downloading
        model.save_pretrained(model_path)
        tokenizer.save_pretrained(model_path)

    # Move model to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

# Asynchronously load the model when the app starts
async def startup_event():
    await load_model()

def generate_response(query, context):
    print(query)
    print(context)
    prompt = f"Instruct: You are a helpful bot who only answers using the given context ONLY. If you cannot find the answer in the context reply 'Sorry don't have that detail'. Given the context '{context}', answer this:{query}\nOutput:"

    with torch.no_grad():
        inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=False, add_special_tokens=False)
        inputs = {name: tensor.to(model.device) for name, tensor in inputs.items()}
        outputs = model.generate(**inputs, max_new_tokens=526, max_length=2000, pad_token_id=tokenizer.eos_token_id)
        
    text = tokenizer.batch_decode(outputs)[0]

    # Remove the prompt from the output text
    text = text.replace(prompt, '').strip()
    text = text.replace("<|endoftext|>", '').strip()
    
    return text