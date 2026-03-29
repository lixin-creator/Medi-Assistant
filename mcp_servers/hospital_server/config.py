"""Configuration for the hospital MCP server."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load backend/.env first so local development can share one env file.
ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_ENV_FILE = ROOT_DIR / 'backend' / '.env'
if BACKEND_ENV_FILE.exists():
    load_dotenv(BACKEND_ENV_FILE, override=False)
load_dotenv(override=False)

AMAP_WEB_SERVICE_KEY = os.getenv('AMAP_WEB_SERVICE_KEY')
HOSPITAL_MCP_SERVER_HOST = os.getenv('HOSPITAL_MCP_SERVER_HOST', '127.0.0.1')
HOSPITAL_MCP_SERVER_PORT = int(os.getenv('HOSPITAL_MCP_SERVER_PORT', '8090'))
