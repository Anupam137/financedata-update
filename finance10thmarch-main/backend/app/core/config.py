import os
from dotenv import load_dotenv

# Force reload of environment variables from .env file
load_dotenv(override=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "")
FINANCIAL_DATASETS_API_KEY = os.getenv("FINANCIAL_DATASETS_API_KEY", "")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")

# API URLs
OPENAI_API_URL = "https://api.openai.com/v1"
POLYGON_API_URL = "https://api.polygon.io"
PERPLEXITY_API_URL = os.getenv("PERPLEXITY_API_URL", "https://api.perplexity.ai")

# Frontend URL for CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://finance10thmarch.vercel.app")

# Database Configuration (for future implementation)
DB_USERNAME = os.getenv("DB_USERNAME", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "financial_search")

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_ENABLED = os.getenv("REDIS_ENABLED", "true").lower() == "true"

# API settings
API_PREFIX = "/api"
API_VERSION = "v1"

# Feature flags
ENABLE_FAST_PATH = os.getenv("ENABLE_FAST_PATH", "true").lower() == "true"
ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
ENABLE_STREAMING = os.getenv("ENABLE_STREAMING", "true").lower() == "true" 