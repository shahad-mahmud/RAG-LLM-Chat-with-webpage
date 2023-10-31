import streamlit as st
import src
from langchain.vectorstores import qdrant
from langchain.chains import RetrievalQA


def main():
    st.title("Ask your web page")

    if "links" not in st.session_state:
        st.session_state["links"] = []

    with st.sidebar:
        option = st.selectbox("Which LLM do you want to use?", ("LLaMA 2", "LLaVA"))

        if option == "LLaMA 2":
            llm = src.llms.get_llama2_chat()
        elif option == "LLaVA":
            llm = src.llms.get_llava_chat()
        else:
            raise ValueError(f"Invalid option: {option}")

        embedder = src.embeddings.get_hf_embedder()

        st.text_input(
            "web page links",
            key="web_page_link_add",
            type="default",
            placeholder="https://",
        )

        if st.session_state.web_page_link_add:
            link = st.session_state.web_page_link_add
            if link and link not in st.session_state.links:
                st.session_state.links.append(link)
                text = src.data.load_text(link, split=True)

                vectorstore = qdrant.Qdrant.from_documents(
                    text, embedder, collection_name="chat_with_page"
                )

        # show the added links
        for i, link in enumerate(st.session_state.links):
            if link:
                st.write(f"{i+1}. {link}")

    if question := st.chat_input(placeholder="Ask your web page"):
        st.chat_message("user").write(question)


if __name__ == "__main__":
    main()
