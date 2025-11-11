from pathlib import Path
from typing import List, Dict
import uuid
from PyPDF2 import PdfReader


class ResumeParser:


    def __init__(self, base_path: str = "/home/moussaoui/langchain-chatbot/data/data"):
        self.base_path = Path(base_path)


    def _extract_text(self, pdf_path) -> str:
        reader = PdfReader(str(pdf_path))
        text = " ".join([page.extract_text() or "" for page in reader.pages])
        return text.strip()


    def parse(self) -> List[Dict]:
        results = []

        for category_dir in sorted(self.base_path.iterdir()):
            if category_dir.is_dir():
                category = category_dir.name.upper()
                print(f"Catégorie détectée : {category}")

                for pdf_file in category_dir.glob("*.pdf"):
                    text = self._extract_text(pdf_file)
                    if not text:
                        continue

                    results.append({
                        "id": str(uuid.uuid4()),  
                        "category": category,     
                        "text": text               
                    })

        print(f"\n Extraction terminée : {len(results)} CVs trouvés.")
        return results
