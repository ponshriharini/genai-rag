import streamlit as st
from utils.file_processing import process_file
from utils.summary import generate_summary
from utils.rag_chain import get_validated_answer
from utils.azure_indexing import index_chunks_to_azure_search

st.title("📄 Document Q&A with Azure AI")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "doc_id" not in st.session_state:
    st.session_state.doc_id = None
if "full_text" not in st.session_state:
    st.session_state.full_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""

uploaded_file = st.file_uploader("Upload a PDF or CSV file", type=["pdf", "csv"])

if uploaded_file and st.session_state.doc_id is None:
    with st.spinner("Processing file..."):
        doc_id, full_text = process_file(uploaded_file)

        with st.spinner("Indexing chunks to Azure Search..."):
            index_chunks_to_azure_search(doc_id, full_text)

        summary = generate_summary(full_text)

        st.session_state.doc_id = doc_id
        st.session_state.full_text = full_text
        st.session_state.summary = summary
        st.session_state.chat_history = []

# Always show document summary
if st.session_state.summary:
    with st.expander("📌 Document Summary", expanded=True):
        st.write(st.session_state.summary)

# Chat interface
if st.session_state.doc_id:
    for pair in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(pair["q"])
        with st.chat_message("assistant"):
            st.markdown(pair["a"])

    # New question input
    if question := st.chat_input("Ask something about the document..."):
        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("Thinking..."):
            answer = get_validated_answer(question)

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.chat_history.append({"q": question, "a": answer})
