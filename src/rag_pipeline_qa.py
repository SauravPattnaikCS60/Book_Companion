from langchain import vectorstores as vs
from langchain import embeddings
import json
from langchain import PromptTemplate
from nltk.tokenize import sent_tokenize
from load_model_and_generate_response import generate_response
from output_parsing import parse_output_for_ui
import re
import warnings
warnings.filterwarnings('ignore')


def preprocess_text(text):
    text = text.lower()
    text = re.sub("[^a-z0-9]"," ",text)
    text = re.sub("(\s)+"," ",text)
    return text

def get_relevant_document_page_content(documents):

    context = ""
    for document in documents:
        context += document.page_content + "\n\n"
    
    return context

def get_prompt(query,context):
    query = f'Based on the context given above please answer the question : {query}'
    template = f'''You are an English literature expert who has solid ability of explaining complex things in a simple manner.

    Context: {context}
    
    Question: {query}

    Answer:'''
    prompt_template = PromptTemplate(
    input_variables=["query","context"],
    template=template)
    prompt = prompt_template.format(query=query,context=context)
    return prompt


def invoke_rag_pipeline_qa(query):
    print('Invoking rag pipeline')
    vectorstore = vs.FAISS
    embedding_model = embeddings.HuggingFaceEmbeddings(model_name='hugging_face_models/cache/sentence-transformers_all-mpnet-base-v2/')
    db = vectorstore.load_local('job_description.index/', embedding_model,allow_dangerous_deserialization=True)
    

    db = db.as_retriever(search_kwargs={'k':4})

    relevant_documents = db.get_relevant_documents(query)
    context = get_relevant_document_page_content(relevant_documents)
    print(context)
    num_sentences = len(sent_tokenize(context))
    num_sentences = min(100,num_sentences//4) ## used for extractive summary module
    json.dump(context,open('intermediate_files/qa_context.txt','w'))
    prompt = get_prompt(query, context)
    json.dump(prompt, open('intermediate_files/qa_prompt.txt','w'))
    output = generate_response(prompt)
    json.dump(output, open('intermediate_files/qa_output.json','w'))
    output = parse_output_for_ui(output)
    return output


if __name__ == '__main__':
    print(invoke_rag_pipeline_qa('Tell me something about James Hutton?'))
