# src/chunking/recursive_chunking.py
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents, chunk_size=500, chunk_overlap=150, verbose=False):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")

    return chunks


def create_chunks(documents, chunk_size=400, chunk_overlap=50, verbose=False):
    return split_documents(documents, chunk_size, chunk_overlap, verbose)

def print_chunks(chunks):
     print("\n===== ALL CREATED CHUNKS =====")
     for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print("Text:", chunk.page_content)
        print("Policy:", chunk.metadata.get("policy"))
        print("Document:", chunk.metadata.get("doc_name"))
        print("Page:", chunk.metadata.get("page_number"))
        print("Start index:", chunk.metadata.get("start_index"))
        print("Length:", len(chunk.page_content))
        print("-" * 60)