from transformers import AutoTokenizer, AutoModelForCausalLM
import os
os.environ['TRANSFORMERS_CACHE'] = './hugging_face_models/cache/'

model_id = "google/gemma-2b-it"
tokenizer = AutoTokenizer.from_pretrained("hugging_face_models\\cache\\models--google--gemma-2b-it\\snapshots\\060189a16d5d2713425599b533a9e8ece8f5cca6\\")
model = AutoModelForCausalLM.from_pretrained("hugging_face_models\\cache\\models--google--gemma-2b-it\\snapshots\\060189a16d5d2713425599b533a9e8ece8f5cca6\\")
                                            

input_text = "Write me a poem about Machine Learning."
input_ids = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**input_ids,max_new_tokens=100)
print(tokenizer.decode(outputs[0]))