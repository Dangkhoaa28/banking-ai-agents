import requests
from app.clients.base import BaseLLMClient
from app.core.settings import settings

class OllamaClient(BaseLLMClient):
    def __init__(self):
        # rstrip('/') để đảm bảo không bị thừa dấu gạch chéo khi nối chuỗi
        self.base_url = settings.OLLAMA_BASE_URL.strip().rstrip('/')
        self.model = settings.MODEL_NAME
        self.timeout = 120  

    def generate(self, prompt: str) -> str:
        """Generate text using Ollama API via /api/chat endpoint."""
        
        url = f"{self.base_url}/api/chat"
        
        # Payload format cho /api/chat (giống ChatGPT API)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        try:
            print(f"📡 Sending request to: {url}")
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            
            # /api/chat trả về format: {"message": {"content": "..."}}
            return result.get("message", {}).get("content", "").strip()
            
        except requests.exceptions.Timeout:
            print(f" Ollama request timed out sau {self.timeout}s.")
            return "Hệ thống đang xử lý hơi chậm, vui lòng đợi trong giây lát."
        except requests.exceptions.RequestException as e:
            print(f" Ollama API error: {e}")
            return "Có lỗi kết nối với AI, vui lòng thử lại sau."
    
    def check_connection(self) -> bool:
        """Kiểm tra xem link Pinggy còn sống không."""
        try:
           
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False