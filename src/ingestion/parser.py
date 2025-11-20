"""
Resume/CV Parser module - Extracts text from PDF files.
Converts PDF resumes into structured data.
"""

import os
from pathlib import Path
from typing import List, Dict
import PyPDF2


class ResumeParser:
    """
    Parses resume/CV PDF files from a directory structure.
    
    Directory structure expected:
    data/
       CATEGORY1/
          resume1.pdf
          resume2.pdf
          ...
       CATEGORY2/
          resume1.pdf
          ...
       ...
    """

    def __init__(self, base_path: str = "src/data"):
        """
        Initialize the parser.
        
        Args:
            base_path: Path to the directory containing category folders
        """
        self.base_path = Path(base_path)
        if not self.base_path.exists():
            raise FileNotFoundError(f"Data path not found: {base_path}")

    def parse(self) -> List[Dict[str, str]]:
        """
        Parse all PDFs in the directory structure.
        
        Returns:
            List of dicts with keys: 'id', 'category', 'text'
        """
        results = []
        
        # Iterate through each category folder
        for category_folder in sorted(self.base_path.iterdir()):
            if not category_folder.is_dir():
                continue
            
            category = category_folder.name
            
            # Iterate through PDF files in the category
            for pdf_file in sorted(category_folder.glob("*.pdf")):
                try:
                    text = self._extract_text_from_pdf(pdf_file)
                    
                    results.append({
                        'id': pdf_file.stem,
                        'category': category,
                        'text': text
                    })
                except Exception as e:
                    print(f"Warning: Could not parse {pdf_file}: {e}")
                    continue
        
        return results

    @staticmethod
    def _extract_text_from_pdf(pdf_path: Path) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text
        """
        text = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
        except Exception as e:
            raise Exception(f"Error extracting text from {pdf_path.name}: {e}")
        
        return "\n".join(text)
