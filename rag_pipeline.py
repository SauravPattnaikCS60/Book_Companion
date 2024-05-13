from langchain import vectorstores as vs
from langchain.prompts import ChatPromptTemplate
from langchain import embeddings
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
from langchain import PromptTemplate

chapter_to_title_mapper={
'1':'How to Build a Universe',
'2':'Welcome to the Solar System ',
'3':'The Reverend Evans\'s Universe',
'4':'The Measure of Things',
'5':'The Stone-Breakers',
'6':'Science Red in Tooth and Claw',
'7':'Elemental Matters',
'8':'Einstein\'s Universe',
'9':'The Mighty Atom',
'10':'Getting the Lead Out',
'11':'Muster Mark\'s Quarks',
'12':'The Earth Moves',
'13':'Bang!',
'14':'The Fire Below',
'15':'Dangerous Beauty',
'16':'Lonely Planet',
'17':'Into the Troposphere',
'18':'THE BOUNDING MAIN',
'19':'THE RISE OF LIFE',
'20':'SMALL WORLD',
'21':'LIFE GOES ON',
'22':'GOOD-BYE TO ALL THAT',
'23':'THE RICHNESS OF BEING',
'24':'CELLS',
'25':'DARWIN’S SINGULAR NOTION',
'26':'THE STUFF OF LIFE',
'27':'Ice Time',
'28':'The Mysterious Biped',
'29':'THE RESTLESS APE',
'30':'GOOD-BYE'   
}

def get_relevant_document_page_content(documents, chapter_number):

    context = ""
    for document in documents:
        if document.metadata['source'] == chapter_number:
            context += document.page_content + "\n\n"
    
    return context

def get_prompt(context, summary_words):
    query = f'Summarize the above text in {summary_words} words.'
    template = f'''You are an English literature expert who has solid ability of explaining complex things in a simple manner.

    Context: {context}
    
    Question: {query}

    Answer:'''
    prompt_template = PromptTemplate(
    input_variables=["query"],
    template=template)
    prompt = prompt_template.format(query=query)
    return prompt

def load_model_and_generate(prompt,summary_words):
    tokenizer = AutoTokenizer.from_pretrained("hugging_face_models\\cache\\models--google--gemma-2b-it\\snapshots\\060189a16d5d2713425599b533a9e8ece8f5cca6\\")
    model = AutoModelForCausalLM.from_pretrained("hugging_face_models\\cache\\models--google--gemma-2b-it\\snapshots\\060189a16d5d2713425599b533a9e8ece8f5cca6\\")
    input_ids = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**input_ids,max_new_tokens=summary_words+25)
    # response = model(prompt)
    return tokenizer.decode(outputs[0])

def invoke_rag_pipeline(chapter_number, summary_words=50):
    chapter_title = chapter_to_title_mapper[str(chapter_number)]
    vectorstore = vs.FAISS
    embedding_model = embeddings.HuggingFaceEmbeddings(model_name='hugging_face_models/cache/sentence-transformers_all-mpnet-base-v2/')
    db = vectorstore.load_local('job_description.index/', embedding_model,allow_dangerous_deserialization=True)
    db = db.as_retriever(search_kwargs={'k':10, 'source':chapter_title})

    relevant_documents = db.get_relevant_documents(chapter_title)
    context = get_relevant_document_page_content(relevant_documents,chapter_number)
    json.dump(context,open('context.txt','w'))
    prompt = get_prompt(context,summary_words)
    json.dump(prompt, open('prompt.txt','w'))
    output = load_model_and_generate(prompt, summary_words)
    json.dump(output, open('output.json','w'))
    return output


print(invoke_rag_pipeline(25,250))