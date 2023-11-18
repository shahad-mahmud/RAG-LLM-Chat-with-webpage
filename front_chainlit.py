import chainlit as cl

import src


@cl.on_chat_start
async def setup():
    cl.user_session.set("links", [])

    llm_chain = src.llms.chains.get_LLMChain(
        prompt=src.prompts.get_simple_prompt(), llm=src.llms.get_llava_chat()
    )

    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def user(user_message: cl.Message):
    message = user_message.content

    if message.startswith("/add"):
        cl.user_session.get("links", []).append(message[5:].strip())
        response = f"Added link: {message[5:].strip()}"
    elif message.startswith("/remove"):
        cl.user_session.get("links", []).remove(message[8:].strip())
        response = f"Removed link: {message[8:].strip()}"
    elif message.startswith("/clear"):
        cl.user_session.set("links", [])
        response = "Cleared all links"
    elif message.startswith("/list"):
        response = f"All added links: {cl.user_session.get('links')}"

    llm_chain = cl.user_session.get("llm_chain")

    response = await llm_chain.acall(
        message, callbacks=[cl.AsyncLangchainCallbackHandler()]
    )
    response = response["text"]

    # response = llm(user_message.content)
    # response = f"All added links: {cl.user_session.get('links')}"
    # response = "Hello"
    await cl.Message(content=response).send()
