from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf_extraction import extract_content
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import json
import os
from config import book_file_mapping, chapter_numbers_mapper,base_path


def chunking_and_splitting(chapter_wise_content,book_name):
    documents = []
    for chapter_number, content in chapter_wise_content.items():
        print(book_name + '_' + str(chapter_number))
        doc = [Document(page_content=content,metadata={'source':book_name+'_'+str(chapter_number)})]
        documents.extend(doc)

    recursive_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024, chunk_overlap=256, separators=r"\n\n"
    )
    documents = recursive_text_splitter.split_documents(documents)
    return documents


def create_db(documents, embedding_model):
    model_vectorstore = FAISS
    db = None
    try:
        db = model_vectorstore.from_documents(documents, embedding_model)
        return db
    except Exception as error:
        print(error)


def create_vectorstore(book_filenames, embedding_model):
    all_documents = []
    for book_name in book_filenames:
        try:
            print(f'Processing Book : {book_name}...')
            book_file_name = book_file_mapping[book_name]
            chapter_numbers = chapter_numbers_mapper[book_name]
            filepath = os.path.join(base_path, book_file_name)
            chapter_wise_content = extract_content(filepath,chapter_numbers)
            documents = chunking_and_splitting(chapter_wise_content, book_name)
            all_documents.extend(documents)
            print(f'Processing completed.')
        except Exception as e:
            print(str(e))
            continue

    print(len(all_documents))
    db = create_db(all_documents, embedding_model)
    return db

if __name__ == "__main__":
    books_filenames = ["Programming Python", "Vikings", "Introduction to ML"]
    embedding_model = HuggingFaceEmbeddings(
        model_name="hugging_face_models/cache/sentence-transformers_all-mpnet-base-v2/"
    )
    database = create_vectorstore(books_filenames, embedding_model)
    database.save_local("books.index")
