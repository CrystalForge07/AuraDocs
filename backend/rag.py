import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

embedding_model = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

def process_pdf(pdf_bytes):
    pdf = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text() + "\n"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    chunks = splitter.split_text(text)

    vectors = embedding_model.embed_documents(chunks)

    text_embeddings = list(zip(chunks, vectors))

    vectorstore = FAISS.from_embeddings(
        text_embeddings,
        embedding_model
    )

    return vectorstore

# Retrieves relevant documents with reference to the question

def retrieve_documents(vectorstore, question, k=4):
    docs = vectorstore.max_marginal_relevance_search(
        question,
        k=k,
        fetch_k=20
    )
    return docs

# Converts the retrieved Document objects into one string

def build_context(docs):
    context = "\n\n".join(doc.page_content for doc in docs)
    return context

def generate_answer(context, question):
    prompt = f"""
    You are AuraDocs, a friendly document question-answering assistant.

    You have access to information retrieved from the user's uploaded document.

    Follow these rules:

    1. If the user is making casual conversation, such as saying hello,
    thanking you, asking what you can do, or making a simple conversational
    statement, respond naturally and helpfully. You do not need to use the
    document context for these messages.

    2. If the user asks a question about the uploaded document:
    - Answer using ONLY the provided document context.
    - Do not use outside knowledge to fill missing information.
    - If the answer cannot be found in the context, say:
        "I couldn't find the answer in the document."
    - If only part of the answer is available, clearly explain what the
        document does and does not provide.

    3. Keep responses concise and natural.

    4. If the user asks what you can do, explain that you can answer questions
    about their uploaded document.

    5. Do not mention embeddings, vector databases, retrieval, chunks,
    or other internal implementation details unless the user asks about them.
    
    Context:
    {context}

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    return response.content

def ask_question(vectorstore, question):
    docs = retrieve_documents(vectorstore, question, k=4)

    context = build_context(docs)

    answer = generate_answer(context, question)

    return answer, docs