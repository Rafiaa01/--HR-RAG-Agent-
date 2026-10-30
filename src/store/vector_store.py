
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.chunking.chunking import create_chunks, print_chunks
from src.loader.load_data import load_pdfs

load_dotenv()


def create_vector_store():
    documents = load_pdfs()
    chunks = create_chunks(documents)
    print_chunks(chunks)

    if not chunks:
        raise ValueError("No chunks found. Check your PDFs and chunking step.")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    print("FAISS index created successfully.")
    print("Total indexed chunks:", vector_store.index.ntotal)

    # TEST: Check metadata after FAISS retrieval
    retriever = get_retriever(vector_store, k=5)

    retrieved_docs = retriever.invoke("annual leave policy")

    for i, doc in enumerate(retrieved_docs, start=1):
        print(f"\n--- Retrieved Chunk {i} ---")
        print("Content:", doc.page_content[:200])
        print("Metadata:", doc.metadata)
        print("Policy:", doc.metadata.get("policy"))
        print("Document:", doc.metadata.get("doc_name"))
        print("Page:", doc.metadata.get("page_number"))

    vector_store.save_local("faiss_index")

    return vector_store


def get_retriever(vector_store, mode="similarity", k=5, policy=None):
    search_kwargs = {"k": k}

    if policy:
        search_kwargs["filter"] = {"policy": policy}

    if mode == "mmr":
        search_kwargs["fetch_k"] = 40
        search_kwargs["lambda_mult"] = 0.5
    elif policy:
        search_kwargs["fetch_k"] = 40

    return vector_store.as_retriever(
        search_type=mode,
        search_kwargs=search_kwargs
    )
