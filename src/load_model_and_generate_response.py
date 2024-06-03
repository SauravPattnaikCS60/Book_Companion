from transformers import AutoTokenizer, AutoModelForCausalLM
from functools import lru_cache


@lru_cache
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("hugging_face_models\\cache\\models--google--gemma-2b-it\\snapshots\\060189a16d5d2713425599b533a9e8ece8f5cca6\\",low_cpu_mem_usage=True,local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained("hugging_face_models\\cache\\models--google--gemma-2b-it\\snapshots\\060189a16d5d2713425599b533a9e8ece8f5cca6\\",low_cpu_mem_usage=True,local_files_only=True)
    return model, tokenizer

def generate_response(prompt, tokens=100):
    model, tokenizer = load_model()
    input_ids = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**input_ids,max_new_tokens=tokens)
    # response = model(prompt)
    return tokenizer.decode(outputs[0])