from pathlib import Path
from typing import List, Dict
import uuid
import re
import joblib   

import pandas as pd

from PyPDF2 import PdfReader
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report



class ResumeParser:
    def __init__(
        self,
        base_path: str = "/home/moussaoui/p2/projet-ia/src/server/backend/data"
    ):
        self.base_path = Path(base_path)

    def _clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _extract_text(self, pdf_path) -> str:
        reader = PdfReader(str(pdf_path))
        text = " ".join(page.extract_text() or "" for page in reader.pages)
        return self._clean_text(text)

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
        print(f"\nExtraction terminée : {len(results)} CVs trouvés.")
        return results



def train_classifier(data: List[Dict]):
    df = pd.DataFrame(data)

    X_text = df["text"]
    y_label = df["category"]

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_label)

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words="english"
    )

    X = vectorizer.fit_transform(X_text)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    clf = LinearSVC(class_weight="balanced")
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print("\n=== RAPPORT DE CLASSIFICATION ===\n")
    print(classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    ))


    Path("models").mkdir(exist_ok=True)

    joblib.dump(clf, "models/svm.joblib")
    joblib.dump(vectorizer, "models/tfidf.joblib")
    joblib.dump(label_encoder, "models/labels.joblib")

    print("\nModèle sauvegardé dans le dossier /models")

    return clf, vectorizer, label_encoder



def predict_pdf(pdf_path, clf, vectorizer, encoder):
    reader = PdfReader(str(pdf_path))
    text = " ".join(page.extract_text() or "" for page in reader.pages)
    text = text.lower()

    X = vectorizer.transform([text])
    pred = clf.predict(X)[0]

    return encoder.inverse_transform([pred])[0]



if __name__ == "__main__":
    DATA_PATH = "/home/moussaoui/p2/projet-ia/src/server/backend/data"

    parser = ResumeParser(DATA_PATH)
    data = parser.parse()

    clf, vectorizer, encoder = train_classifier(data)

    test_pdf = "/home/moussaoui/p2/projet-ia/src/server/ml_pipeline/cv.pdf"
    if Path(test_pdf).exists():
        metier = predict_pdf(test_pdf, clf, vectorizer, encoder)
        print(f"\nMétier prédit : {metier}")
