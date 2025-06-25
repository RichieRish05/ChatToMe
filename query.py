import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import warnings
import textwrap

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Only answer questions pertaining to Rishi Murumkar and his life. Your name is Cubby, a lion cub whose only goal
is to make the user experience of my personal portofolio better. You are personable and professional.
___
{context}

---

Answer the question based on the above information: {question}
"""


def query_model(query_text):
    warnings.filterwarnings('ignore') # Ignore warnings


    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(
        model="text-embedding-ada-002"
    )
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    print(f"Number of documents in database: {db._collection.count()}")

    # Search the DB with more documents and lower relevance threshold
    results = db.similarity_search_with_relevance_scores(
        query_text,
        k=2, 
        score_threshold=0.3  # Lowered threshold to 0.1
    )
    
    # Add debugging information
    if not results:
        print("No results found with current threshold. Try lowering it further.")
        return "I apologize, but I couldn't find any relevant information in my knowledge base to answer your question."
    
    # Format context with relevance scores for better context
    context_parts = []
    for doc, score in results:
        context_parts.append(f"Relevance: {score:.2f}\n{doc.page_content}")
    
    context_text = "\n\n---\n\n".join(context_parts)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI()
    response_text = model.invoke(prompt)

    return response_text.content


if __name__ == "__main__":
    print(query_model("Tell me about Rishi"))