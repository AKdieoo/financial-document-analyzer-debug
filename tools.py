from crewai.tools import tool
from langchain_community.document_loaders import PyPDFLoader
import os


@tool
def read_data_tool(path: str) -> str:
    """
    Reads and extracts text from a financial PDF file.

    The input must be a valid file path string.
    """

    if not isinstance(path, str):
        raise ValueError("The 'path' argument must be a string.")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found at {path}")
    
    docs = PyPDFLoader(path).load()

    full_report = ""
    for data in docs:
        content = data.page_content
        while "\n\n" in content:
            content = content.replace("\n\n", "\n")
        full_report += content + "\n"

    return full_report[:8000]  # optional safety limit