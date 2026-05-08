import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class EmbeddingsService:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None

    def preload(self):
        try:
            logger.info(f"Pre-loading Sentence Transformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Sentence Transformer model: {str(e)}")

    def get_embeddings(self, text):
        if self.model is None:
            self.preload()
        return self.model.encode(text).tolist()

embeddings_service = EmbeddingsService()
