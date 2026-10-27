import os
from pathlib import Path
from typing import List

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

class Settings:
    PROJECT_NAME: str = "AML Cross-Border Transaction Monitoring System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/aml_database.db")
    
    # ML Artifacts directory: check PROJECT_ROOT/ml/artifacts, BASE_DIR/ml/artifacts, or env var
    ML_ARTIFACTS_DIR: Path = Path(
        os.getenv(
            "ML_ARTIFACTS_DIR",
            str(PROJECT_ROOT / "ml" / "artifacts") if (PROJECT_ROOT / "ml" / "artifacts").exists()
            else str(BASE_DIR / "ml" / "artifacts")
        )
    )
    
    LIGHTGBM_MODEL_PATH: Path = ML_ARTIFACTS_DIR / "lightgbm_model.pkl"
    PREPROCESSOR_PATH: Path = ML_ARTIFACTS_DIR / "preprocessor.pkl"
    FEATURE_NAMES_PATH: Path = ML_ARTIFACTS_DIR / "processed_feature_names.pkl"
    MODEL_CONFIG_PATH: Path = ML_ARTIFACTS_DIR / "model_config.pkl"
    
    # ML Inference Parameters
    CLASSIFICATION_THRESHOLD: float = 0.50
    
    # CORS Origins (comma-separated env var or wildcard)
    _raw_cors = os.getenv("CORS_ORIGINS", "*")
    CORS_ORIGINS: List[str] = [orig.strip() for orig in _raw_cors.split(",")] if _raw_cors != "*" else ["*"]

settings = Settings()
