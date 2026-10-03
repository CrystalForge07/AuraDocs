import hashlib
import streamlit as st
from backend.rag import process_pdf, ask_question

# Page configuration

st.set_page_config(
    page_title="AuraDocs",
    page_icon="⭐",
    layout="centered"
)

with st.sidebar:
    st.header("⭐ AuraDocs")
    st.write("Your private document Q&A assistant.")

    st.divider()

    st.subheader("How it works :")
    st.write("1. Upload a PDF")
    st.write("2. Ask a question")
    st.write("3. Get an answer from your document")
    st.divider()
    st.caption("Created by Abhishek Godbole.")

# Session state

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "file_hash" not in st.session_state:
    st.session_state.file_hash = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# UI

st.title("⭐ AuraDocs")
st.caption("Ask questions about your documents.")

st.divider()

# PDF Upload

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    help="Upload a text-based PDF for the best results."
)

if uploaded_file is not None:

    pdf_bytes = uploaded_file.getvalue()

    # Create an unique identifier for this uploaded file
    file_hash = hashlib.sha256(pdf_bytes).hexdigest()

    # Process only if this is a new PDF
    if file_hash != st.session_state.file_hash:

        with st.spinner("Processing your PDF..."):

            try:
                vectorstore = process_pdf(pdf_bytes)
            except Exception as e:
                st.error("Something went wrong while processing this PDF.")
                st.stop()

            st.session_state.vectorstore = vectorstore
            st.session_state.file_hash = file_hash
            st.session_state.file_name = uploaded_file.name

            # Clear previous conversation
            st.session_state.messages = []

        st.success(f"✅ **{uploaded_file.name}** is ready to chat!")

# Show current document

if st.session_state.vectorstore is not None:

    # Display chat history

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Question input

    question = st.chat_input(
        "Ask a question about your document..."
    )

    if question and question.strip():

        # Display user's question
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)


        # Get answer from backend
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:
                    answer, docs = ask_question(
                        st.session_state.vectorstore,
                        question
                    )
                except Exception:
                    st.error("Something went wrong.")
                    st.stop()

            st.markdown(answer)


        # Save answer to chat history
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

else:
    st.info("📄 Upload a PDF above to start asking questions.")