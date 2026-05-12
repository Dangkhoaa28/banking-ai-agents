"""
Entry point for the Banking AI-Agent FastAPI server.
"""
import warnings
import uvicorn
import sys
from app.core.settings import settings

# Suppress non-critical warnings
warnings.filterwarnings("ignore", message=".*max_new_tokens.*max_length.*")
warnings.filterwarnings("ignore", message=".*clean_up_tokenization_spaces.*")
warnings.filterwarnings("ignore", category=FutureWarning)

def main():
    print("\n" + "="*60)
    print("🚀 Banking AI-Agent Server Startup")
    print("="*60)
    print(f"\n📡 Configuration:")
    print(f"   Ollama URL: {settings.OLLAMA_BASE_URL}")
    print(f"   Model: {settings.MODEL_NAME}")
    print(f"   Intent Model: {settings.LAB_2_MODEL_PATH}")
    
    print(f"\n🌐 API Server:")
    print(f"   Host: {settings.API_HOST}")
    print(f"   Port: {settings.API_PORT}")
    print(f"   URL: http://{settings.API_HOST if settings.API_HOST != '0.0.0.0' else 'localhost'}:{settings.API_PORT}")
    
    print(f"\n📚 Interactive Docs:")
    print(f"   Swagger UI: http://localhost:{settings.API_PORT}/docs")
    print(f"   ReDoc: http://localhost:{settings.API_PORT}/redoc")
    
    print(f"\n🧪 Testing:")
    print(f"   Run: python test_api.py")
    
    print("\n" + "="*60)
    print("Starting server...\n")
    
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.API_HOST,
            port=settings.API_PORT,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n⛔ Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
