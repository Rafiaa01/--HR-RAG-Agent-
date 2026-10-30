
from langchain.tools import tool
from src.store.vector_store import create_vector_store, get_retriever

vector_store = create_vector_store()
retriever = get_retriever(vector_store, mode="similarity", k=5)


@tool
def search_company_policy(query: str) -> str:
    """
    Search company HR policy documents for relevant information.
    Use this tool for questions about annual leave, remote work,
    employee benefits, and company policies.
    """
    if not query.strip():
        return "Please provide a valid policy question."

    documents = retriever.invoke(query)

    if not documents:
        return "No relevant policy information found."

    results = []

    for i, doc in enumerate(documents, start=1):
        results.append(
            f"Retrieved Chunk: {i}\n"
            f"Policy: {doc.metadata.get('policy', 'Unknown')}\n"
            f"Document: {doc.metadata.get('doc_name', 'Unknown')}\n"
            f"Page: {doc.metadata.get('page_number', 'Unknown')}\n"
            f"Content: {doc.page_content}"
        )

    return "\n\n---\n\n".join(results)
