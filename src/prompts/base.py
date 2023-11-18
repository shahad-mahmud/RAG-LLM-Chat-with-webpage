from langchain.prompts import PromptTemplate


def get_simple_prompt():
    prompt_template = """
        You are a very helpful and politer friend of the user. The user is asking you
        a question. You are trying to help the user by answering the question. If you
        don't know the answer, just say that you don't know, don't try to make
        up an answer.

        Question: {question}
        Answer:
        """

    return PromptTemplate(template=prompt_template, input_variables=["question"])


def get_retrival_prompt():
    promt_template = """
        Use the following pieces of context to answer the question at the end. If you
        don't know the answer, just say that you don't know, don't try to make up an
        answer. If the user wants a code, write it in ```CODE BLOCK```.

        {context}

        Question: {question}

        Always be polite and respectful. If the user is rude, don't be rude back.
        If the user is being rude, just say that you don't want to talk to them
        anymore and end the conversation.
        """

    return PromptTemplate(
        template=promt_template, input_variables=["context", "question"]
    )
