

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer
from pathlib import Path


class Embedder:
    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent  

        model_path = BASE_DIR / "onnx_model/model.onnx"
        tokenizer_path = BASE_DIR / "onnx_model/tokenizer.json"

        # Vérifications
        if not model_path.exists():
            raise FileNotFoundError(f"model.onnx introuvable à : {model_path}")

        if not tokenizer_path.exists():
            raise FileNotFoundError(f"tokenizer.json introuvable à : {tokenizer_path}")

        print(f"🔍 Chargement modèle ONNX : {model_path}")
        self.session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])

        print(f"🔍 Chargement tokenizer : {tokenizer_path}")
        self.tokenizer = Tokenizer.from_file(str(tokenizer_path))


    def encodeText(self, text: str):
        encoded = self.tokenizer.encode(text)

        input_ids = np.array([encoded.ids], dtype=np.int64)
        attention_mask = np.array([[1] * len(encoded.ids)], dtype=np.int64)
        token_type_ids = np.zeros_like(input_ids, dtype=np.int64)

        ort_inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids
        }

        outputs = self.session.run(None, ort_inputs)

        embedding = outputs[0].mean(axis=1)[0]

        return embedding



    def encodeBatch(self, texts):
        ids = []
        masks = []

        for t in texts:
            encoded = self.tokenizer.encode(t)
            ids.append(encoded.ids)
            masks.append([1] * len(encoded.ids))

        max_len = max(len(x) for x in ids)

        input_ids = np.array([x + [0]*(max_len - len(x)) for x in ids])
        attention_mask = np.array([m + [0]*(max_len - len(m)) for m in masks])
        token_type_ids = np.zeros_like(input_ids)

        ort_inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids
        }

        outputs = self.session.run(None, ort_inputs)

        # outputs[0] = (batch, seq_len, dim)
        # mean pooling -> (batch, dim)
        embeddings = outputs[0].mean(axis=1)

        return embeddings

