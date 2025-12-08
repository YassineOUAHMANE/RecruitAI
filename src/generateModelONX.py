from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForFeatureExtraction

model_name = "sentence-transformers/all-MiniLM-L6-v2"

print("Downloading model…")

# Export ONNX
model = ORTModelForFeatureExtraction.from_pretrained(
    model_name,
    export=True
)

model.save_pretrained("./onnx_model")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained("./onnx_model")

print("ONNX model exported → ./onnx_model/")
