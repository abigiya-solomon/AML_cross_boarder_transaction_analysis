import joblib
import logging
from pathlib import Path
from app.config import settings

logger = logging.getLogger(__name__)

class ModelLoader:
    _instance = None
    
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.feature_names = None
        self.model_config = None
        self.is_loaded = False
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ModelLoader()
        return cls._instance

    def load(self):
        """Loads model and preprocessing artifacts once at startup."""
        if self.is_loaded:
            return

        logger.info(f"Loading ML artifacts from: {settings.ML_ARTIFACTS_DIR}")
        
        # Check files exist
        for path, name in [
            (settings.LIGHTGBM_MODEL_PATH, "lightgbm_model.pkl"),
            (settings.PREPROCESSOR_PATH, "preprocessor.pkl"),
            (settings.FEATURE_NAMES_PATH, "processed_feature_names.pkl"),
            (settings.MODEL_CONFIG_PATH, "model_config.pkl"),
        ]:
            if not path.exists():
                raise FileNotFoundError(f"Missing required ML artifact: {name} at {path}")

        self.model = joblib.load(settings.LIGHTGBM_MODEL_PATH)
        self.preprocessor = joblib.load(settings.PREPROCESSOR_PATH)
        self.feature_names = joblib.load(settings.FEATURE_NAMES_PATH)
        self.model_config = joblib.load(settings.MODEL_CONFIG_PATH)

        self.is_loaded = True
        logger.info(f"Model successfully loaded. Features count: {len(self.feature_names)}")

model_loader = ModelLoader.get_instance()
