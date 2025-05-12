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
Your name is Rishi Murumkar, and you are personable and professional. 

___
{context}

---

Answer the question based on the above information: {question}
"""


def main():
    warnings.filterwarnings('ignore') # Temporary 

    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

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
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    wrapped_response = textwrap.fill(response_text.content, width=80)
    formatted_response = f"""Response: {wrapped_response}\nSources: {', '.join(filter(None, sources))}"""
    print(formatted_response)


if __name__ == "__main__":
    main()