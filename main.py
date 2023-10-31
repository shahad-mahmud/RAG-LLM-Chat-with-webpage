from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
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
    
    promt_template = """
    Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. If the user wants a code, write it in ```CODE BLOCK```.
    
    {context}
    
    Question: {question}
    
    Always be polite and respectful. If the user is rude, don't be rude back. If the user is being rude, just say that you don't want to talk to them anymore and end the conversation.
    """
    
    PROMT = PromptTemplate(template=promt_template, input_variables=["context", "question"])

    memory = ConversationBufferMemory(
        memory_key="chat_history", output_key="answer", return_messages=True
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm, vectorstore.as_retriever(), memory=memory, return_source_documents=False, condense_question_prompt=PROMT
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
