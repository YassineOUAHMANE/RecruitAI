# import numpy as np
# import onnxruntime as ort
# from tokenizers import Tokenizer
# from pathlib import Path


# # ============================================================
# #                 EMBEDDER — VERSION CORRIGÉE
# # ============================================================

# class Embedder:
#     def __init__(self):
#         # Répertoire actuel = .../backend/embeddings
#         BASE_DIR = Path(__file__).resolve().parent

#         model_path = BASE_DIR / "onnx_model/model.onnx"
#         tokenizer_path = BASE_DIR / "onnx_model/tokenizer.json"

#         # Sécurité
#         if not model_path.exists():
#             raise FileNotFoundError(f" model.onnx introuvable à : {model_path}")

#         if not tokenizer_path.exists():
#             raise FileNotFoundError(f" tokenizer.json introuvable à : {tokenizer_path}")

#         print(" Chargement du modèle ONNX...")
#         self.session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])

#         print(" Chargement du tokenizer JSON...")
#         self.tokenizer = Tokenizer.from_file(str(tokenizer_path))

#     # -----------------------------------------------------

#     def encodeText(self, text):
#         encoded = self.tokenizer.encode(text)

#         input_ids = np.array([encoded.ids], dtype=np.int64)
#         attention_mask = np.array([[1] * len(encoded.ids)], dtype=np.int64)
#         token_type_ids = np.zeros_like(input_ids, dtype=np.int64)  #  FIX

#         ort_inputs = {
#             "input_ids": input_ids,
#             "attention_mask": attention_mask,
#             "token_type_ids": token_type_ids
#         }

#         outputs = self.session.run(None, ort_inputs)
#         return outputs[0][0]

#     # -----------------------------------------------------

#     def encodeBatch(self, texts):
#         ids = []
#         masks = []

#         for t in texts:
#             encoded = self.tokenizer.encode(t)
#             ids.append(encoded.ids)
#             masks.append([1] * len(encoded.ids))

#         max_len = max(len(i) for i in ids)

#         ids = np.array([i + [0] * (max_len - len(i)) for i in ids], dtype=np.int64)
#         masks = np.array([m + [0] * (max_len - len(m)) for m in masks], dtype=np.int64)
#         token_type_ids = np.zeros_like(ids, dtype=np.int64)  #  FIX

#         ort_inputs = {
#             "input_ids": ids,
#             "attention_mask": masks,
#             "token_type_ids": token_type_ids
#         }

#         outputs = self.session.run(None, ort_inputs)
#         return outputs[0]



# # ============================================================
# #                        TESTS
# # ============================================================

# def test_single_text(embedder):
#     print("\n=== Test encodeText ===")
#     text = "Hello, this is a test for ONNX embeddings!"
#     vec = embedder.encodeText(text)
#     print("Vector shape:", vec.shape)
#     print("First 10 values:", vec[:10])


# def test_batch(embedder):
#     print("\n=== Test encodeBatch ===")
#     texts = [
#         "I love machine learning.",
#         "This ONNX model should encode without PyTorch.",
#         "Testing batch mode!"
#     ]
#     vecs = embedder.encodeBatch(texts)
#     print("Batch shape:", vecs.shape)
#     print("Row 0 first 10 values:", vecs[0][:10])


# # ============================================================
# #                        MAIN
# # ============================================================

# if __name__ == "__main__":
#     print("\n=== Test ONNX Embedder ===")

#     emb = Embedder()

#     test_single_text(emb)
#     test_batch(emb)

#     print("\n TEST TERMINÉ — AUCUN TORCH UTILISÉ ")
