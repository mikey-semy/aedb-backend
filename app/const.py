from enum import Enum
from typing import Final, Dict, Any, List
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from starlette.types import ASGIApp
from app.core.config import config
from app.version import __version__


# Application params
app_title: Final[str] = "AEDB"
app_description: Final[str] = ""

app_params:   Final[Dict[str, Any]] = {
    "title": app_title, 
    "description": app_description,
    "version": __version__,
    "swagger_ui_parameters": {"defaultModelsExpandDepth": -1},
    "root_path": ""
    }

# Router params
api_prefix: str = f"/api/{__version__}"

# Uvicorn params
host: Final = "0.0.0.0"
port: Final = 8000

uvicorn_params:   Final[Dict[str, Any]] = {
    "host": host, 
    "port": port,
    "proxy_headers": True,
    # "forwarded-allow-ips": "*"
    }

# AWS S3 params
aws_access_key_id: Final = config.aws_access_key_id
aws_secret_access_key: Final = config.aws_secret_access_key
aws_region: Final = config.aws_region
endpoint_url: Final = config.aws_endpoint

s3_params:   Final[Dict[str, Any]] = {
    "aws_access_key_id": aws_access_key_id,
    "aws_secret_access_key": aws_secret_access_key,
    "region_name": aws_region,
    "endpoint_url": endpoint_url
}

# Paths params

# File names
env_file_name:          Path    =   Path('.env')

# Folder names
app_folder_name:        Path    =   Path('app')
templates_folder_name:  Path    =   Path('templates')
static_folder_name:     Path    =   Path('static')


# Paths
main_path:              Path    =   Path(__file__).resolve().parents[1]
env_path:               Path    =   main_path / env_file_name
app_path:               Path    =   main_path / app_folder_name
templates_path:         Path    =   app_path / templates_folder_name
static_path:            Path    =   app_path / static_folder_name


# Main service constants
main_tags: Final[List[str | Enum] | None] = ["Main"]

main_params:   Final[Dict[str, Any]] = {
    "tags": main_tags
    }

# Authentication service constants
auth_tags: Final[List[str | Enum] | None] = ["Authentication"]
auth_url: Final = "token"

auth_params:   Final[Dict[str, Any]] = {
    "prefix": f"/{auth_url}", 
    "tags": auth_tags
    }


# Token constants
token_type: Final = "bearer"
token_algorithm: Final = "HS256"
token_expire_minutes: Final = 60

# Storage service constants
storage_tags: Final[List[str | Enum] | None] = ["Storage"]
storage_url: Final = "storage"

storage_params:   Final[Dict[str, Any]] = {
    "prefix": f"/{storage_url}", 
    "tags": storage_tags
    }

# Converters service constants
converters_tags: Final[List[str | Enum] | None] = ["Converters"]
converters_url: Final = "converters"

converters_params:   Final[Dict[str, Any]] = {
    "prefix": f"/{converters_url}", 
    "tags": converters_tags
    }

# Posts service constants
post_tags: Final[List[str | Enum] | None] = ["Posts"]
post_url: Final = "posts"

post_params:   Final[Dict[str, Any]] = {
    "prefix": f"/{post_url}", 
    "tags": post_tags
    }

# Manuals service constants
manual_tags: Final[List[str | Enum] | None] = ["Manuals"]
manual_url: Final = "manuals"

manual_params:   Final[Dict[str, Any]] = {
    "prefix": f"/{manual_url}", 
    "tags": manual_tags
    }

# Static params
static_path_str: str = "/static"
static_app: ASGIApp = StaticFiles(directory=static_path)
static_name: str = "static"

static_params: Final[Dict[str, Any]] = {
    "path": static_path_str, 
    "app": static_app, 
    "name": static_name
}
