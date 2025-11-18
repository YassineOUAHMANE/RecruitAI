import requests

class HttpService:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"

    def get(self, endpoint: str, params: dict = None):
        # Simulate a GET request
        print(f"GET request to {self.base_url}{endpoint} with params {params}")
        return {"status": "success", "data": "Sample GET response"}

    def query_bot(self, user_query: str):
        payload = {
            "index": 0,
            "content": user_query
        }
        response = requests.post(self.base_url + "/bot-reply", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Request failed with status code {response.status_code}"}
    
    def upload_pdf(self, uploaded):
        
        uploaded.seek(0)

        files = {
            "file": (uploaded.name, uploaded, "application/pdf")
            # Alternatively: ("name", uploaded.getvalue(), "application/pdf")
        }

        try:
            resp = requests.post(self.base_url + "/upload-pdf", files=files, timeout=60)
            if resp.ok:
                return " PDF uploaded successfully."
            else:
                return f"Upload failed: {resp.status_code} {resp.text}"
        except Exception as e:
            return f"Request error: {e}"


api_service = HttpService()
        