from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import qdrant

import src

if __name__ == "__main__":
    links = [
        "https://huggingface.co/docs/transformers/model_doc/bert",
    ]

    llm = src.llms.get_llava_chat()

    texts = src.data.load_text(links, split=True)

    embedder = src.embeddings.get_hf_embedder()
    vectorstore = qdrant.Qdrant.from_documents(texts, embedder)

    memory = ConversationBufferMemory(
        memory_key="chat_history", output_key="answer", return_messages=True
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm, vectorstore.as_retriever(), memory=memory, return_source_documents=False
    )

    while True:
        prompt = input("Question (type `exit` to finish): ")

        if prompt.lower().strip() == "exit":
            break

        result = chain(
            {
                "question": prompt,
            }
        )

        print(result["answer"])
        print("-" * 88)
        print()
