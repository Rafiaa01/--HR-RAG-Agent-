import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

DATA_DIR = Path("src/data")

# policy key -> file name. The key is what you pass to the metadata filter.
POLICY_FILES = {
    "leave": "fictional_employee_policies.pdf",
    "remote": "remote_work_policy.pdf",
    "benefits": "employee_benefits_policy.pdf",
}


def load_pdfs(policy_files=POLICY_FILES, data_dir=DATA_DIR):
    all_documents = []

    for policy_key, file_name in policy_files.items():
        pdf_path = data_dir / file_name

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found at: {pdf_path.resolve()}")

        pages = PyPDFLoader(str(pdf_path)).load()

        if not pages:
            raise ValueError(f"No pages were extracted from: {pdf_path.name}")

        for page in pages:
            page.page_content = re.sub(r"\s+", " ", page.page_content).strip()
            page.metadata["policy"] = policy_key          # used for filtering
            page.metadata["doc_name"] = pdf_path.name     # used for citations
            page.metadata["page_number"] = page.metadata["page"] + 1  # 1-based

        print(f"Loaded {len(pages)} pages from {pdf_path.name}")
        all_documents.extend(pages)

    print(f"Total pages loaded: {len(all_documents)}")
    return all_documents


