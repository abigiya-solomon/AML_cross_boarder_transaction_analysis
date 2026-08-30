import os

class Settings:
    PROJECT_NAME: str = "AML Cross-Border Transaction Analysis System"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    ML_ARTIFACTS_DIR: str = os.path.join(BASE_DIR, "ml", "artifacts")
    
    MODEL_PATH: str = os.path.join(ML_ARTIFACTS_DIR, "lightgbm_model.pkl")
    PREPROCESSOR_PATH: str = os.path.join(ML_ARTIFACTS_DIR, "preprocessor.pkl")
    FEATURE_NAMES_PATH: str = os.path.join(ML_ARTIFACTS_DIR, "processed_feature_names.pkl")
    CONFIG_PATH: str = os.path.join(ML_ARTIFACTS_DIR, "model_config.pkl")
    
    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'backend', 'aml_database.db')}"
    
    PREDICTION_THRESHOLD: float = 0.50

settings = Settings()
