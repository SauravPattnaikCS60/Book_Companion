from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf_extraction import extract_content
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import json

# def create_and_load_vectorstore():

def chunking_and_splitting():
    chapter_wise_content = extract_content()
    json.dump(chapter_wise_content, open('intermediate_files/chapter_wise_content.json','w'))
    documents = []
    for _, content in chapter_wise_content.items():
        doc = [Document(page_content=content)]
        documents.extend(doc)
    
    recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024,chunk_overlap=256,separators=r"\n\n")
    documents = recursive_text_splitter.split_documents(documents)
    return documents

def create_db(documents, embedding_model):
    model_vectorstore = FAISS
    db = None
    try:
        db = model_vectorstore.from_documents(documents,embedding_model)
        return db
    except Exception as error:
        print(error)

documents = chunking_and_splitting()
print(len(documents))

embedding_model = HuggingFaceEmbeddings(model_name='hugging_face_models/cache/sentence-transformers_all-mpnet-base-v2/')
db = create_db(documents,embedding_model)
db.save_local('job_description.index')