import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.embeddings_service import embeddings_service

def test_embeddings():
    print("Pre-loading model...")
    embeddings_service.preload()
    
    text = "Privacy is a fundamental right."
    print(f"Generating embeddings for: '{text}'")
    emb = embeddings_service.get_embeddings(text)
    
    print(f"Embeddings generated! Dimension: {len(emb)}")
    if len(emb) > 0:
        print("✅ Embeddings service is functional.")
    else:
        print("❌ Embeddings service failed.")

if __name__ == "__main__":
    test_embeddings()
