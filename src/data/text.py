from typing import List

from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_text(urls: List[str] = None, split: bool = False):
    if urls:
        loader = WebBaseLoader(urls)

    documents = loader.load()

    if split:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=32)
        documents = splitter.split_documents(documents)

    return documents
