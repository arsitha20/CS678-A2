from typing import Optional, AnyStr, Union, Type, Any
from gentopia.tools.utils.docstore import Docstore, Document
from gentopia.tools.basetool import BaseTool
from PyPDF2 import PdfReader
from pydantic import BaseModel, Field
import requests


class PDFDocstore(Docstore):
    """Wrapper around PyPDF2 for reading and summarizing PDFs."""

    def fetch_and_read_pdf(self, url: str) -> Union[str, Document]:
        """Fetch the PDF from the URL and extract its content."""
        try:
            response = requests.get(url)
            with open("temp.pdf", "wb") as f:
                f.write(response.content)

            reader = PdfReader("temp.pdf")
            text = ""
            for page in reader.pages:
                text += page.extract_text()
                
            result = text
        except Exception as e:
            result = f"An error occurred: {str(e)}"
        return result

    def search(self, query: str) -> str:
        """Placeholder search method to fulfill abstract class requirement."""
        return "Search functionality is not implemented for PDF reading."


class PDFReaderArgs(BaseModel):
    url: str = Field(..., description="URL of the PDF file to fetch and read")


class PDFReader(BaseTool):
    """Tool that adds the capability to read PDF files from a given URL."""

    name = "pdf_reader"
    description = "Fetches and reads a PDF from a given URL."
    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs
    doc_store: Any = None

    def _run(self, url: AnyStr) -> str:
        if not self.doc_store:
            self.doc_store = PDFDocstore() 
        tool = self.doc_store
        evidence = tool.fetch_and_read_pdf(url)
        return evidence  

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
