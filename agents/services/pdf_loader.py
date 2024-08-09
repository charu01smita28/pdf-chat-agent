from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from logger import logging

class PDFLoaderService:
    # def __init__(self):
    #     # self._loader = PyPDFLoader()
    #     pass

    def extract_text(self, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 500):
        """
        Extract and chunk text from the PDF.

        :param file_path: Path to the PDF file.
        :param chunk_size: The maximum size of each text chunk.
        :return: A list of text chunks.
        """
        logging.info("Extracting and chunking text from PDF...")

        # Initialize PyPDFLoader with the provided file path
        loader = PyPDFLoader(file_path)

        # Load the text and chunk it
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        splits = text_splitter.split_documents(docs)

        return splits