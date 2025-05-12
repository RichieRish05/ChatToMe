import json


class JSONTextSplitter:

    def __init__(self, data_path):
        self.data_path = data_path


    def split_text(self):
        with open(self.data_path, "r") as f:
            data = json.load(f)
            chunks = [
                f"Q: {item['question']}\nA: {item['answer']}"
                for item in data
            ]
            return chunks

            