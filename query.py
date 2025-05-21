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
Answer in the first person. Your name is Rishi Murumkar, and you are personable and professional.

___
{context}

---

Answer the question based on the above information: {question}
"""


def query(query_text):
    warnings.filterwarnings('ignore') # Ignore warnings


    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    

    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI()
    response_text = model.invoke(prompt)

    # Format the response with sources
    wrapped_response = textwrap.fill(response_text.content, width=80)
    formatted_response = f"""Response: {wrapped_response}"""
    print(formatted_response)

    return {"response": response_text}


if __name__ == "__main__":
    query("What projects have you worked on?")