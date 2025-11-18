import requests
from http_service import HttpService

# print("Testing HttpService...")

# httpservice = HttpService()

# response = httpservice.query_bot("Hello, how are you?")

# print(response)


# test pdf upload
url = "http://127.0.0.1:8000/upload-pdf"

with open("frontend/testPdf.pdf", "rb") as f:
    files = {"file": ("testPdf.pdf", f, "application/pdf")}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())