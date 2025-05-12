import json
from langchain.docstore.document import Document


class JSONTextSplitter:

    def __init__(self, data_path):
        self.data_path = data_path


    def split_text(self):
        chunks = []

        with open(self.data_path, "r") as f:
            data = json.load(f)
            for item in data:
                chunks.append(Document(
                    page_content=f"{item['question']}\n{item['answer']}",
                    metadata={"id": item['id'], "question": item['question'] }
                ))



            return chunks

if __name__ == '__main__':
    splitter = JSONTextSplitter('/Users/rishi/ChatToMe/data/qa_database.json')
    print(splitter.split_text())