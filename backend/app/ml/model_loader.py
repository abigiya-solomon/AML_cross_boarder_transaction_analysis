import os
import joblib
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class ModelLoader:
    _instance = None

    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.feature_names = None
        self.config = None
        self.is_loaded = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ModelLoader()
        return cls._instance

    def load_artifacts(self):
        if self.is_loaded:
            return

        logger.info("Loading ML artifacts from: %s", settings.ML_ARTIFACTS_DIR)

        if not os.path.exists(settings.MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {settings.MODEL_PATH}")
        if not os.path.exists(settings.PREPROCESSOR_PATH):
            raise FileNotFoundError(f"Preprocessor file not found: {settings.PREPROCESSOR_PATH}")
        if not os.path.exists(settings.FEATURE_NAMES_PATH):
            raise FileNotFoundError(f"Feature names file not found: {settings.FEATURE_NAMES_PATH}")

        self.model = joblib.load(settings.MODEL_PATH)
        self.preprocessor = joblib.load(settings.PREPROCESSOR_PATH)
        self.feature_names = joblib.load(settings.FEATURE_NAMES_PATH)

        if os.path.exists(settings.CONFIG_PATH):
            self.config = joblib.load(settings.CONFIG_PATH)
        else:
            self.config = {
                "model_name": "LightGBM",
                "threshold": settings.PREDICTION_THRESHOLD,
                "number_of_features": len(self.feature_names),
                "target_column": "Is Laundering"
            }

        self.is_loaded = True
        logger.info(
            "Successfully loaded %s model with %d features.",
            self.config.get("model_name", "LightGBM"),
            len(self.feature_names)
        )

model_loader = ModelLoader.get_instance()
