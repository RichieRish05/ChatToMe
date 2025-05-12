from openai import OpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai 
from dotenv import load_dotenv
import os
import shutil
from custom_text_splitter import JSONTextSplitter

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


CHROMA_PATH = "chroma"
DATA_PATH = "data/qa_database.json"


def main():
    generate_data_store()


def generate_data_store():
    chunks = split_text(DATA_PATH)
    save_to_chroma(chunks)

"""
def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents
"""


def split_text(data_path):
    text_splitter = JSONTextSplitter(data_path)
    chunks = text_splitter.split_text()
    print(f"Split data into {len(chunks)} chunks.")


    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Initialize embeddings with the correct configuration
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, embeddings, persist_directory=CHROMA_PATH
    )
    
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()