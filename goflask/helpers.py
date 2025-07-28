"""
GoFlask Helper Functions - Flask-compatible utilities
"""

import json
from typing import Any, Dict, Optional, Union
from .core import GoFlaskResponse


def jsonify(**kwargs) -> GoFlaskResponse:
    """Create JSON response (Flask compatible)"""
    return GoFlaskResponse(kwargs)


def make_response(data: Any, status: int = 200, headers: Optional[Dict[str, str]] = None) -> GoFlaskResponse:
    """Make response (Flask compatible)"""
    return GoFlaskResponse(data, status, headers)


def abort(code: int, description: Optional[str] = None):
    """Abort request with error code"""
    error_message = description or f"HTTP {code}"
    raise Exception(f"HTTP {code}: {error_message}")


def redirect(location: str, code: int = 302):
    """Redirect to location"""
    return GoFlaskResponse(
        data={"redirect": location}, 
        status=code,
        headers={"Location": location}
    )


def url_for(endpoint: str, **values):
    """Generate URL for endpoint (simplified)"""
    # Basic implementation - in full version would use proper URL building
    return f"/{endpoint}"


def flash(message: str, category: str = "message"):
    """Flash a message (Flask compatible)"""
    # Basic implementation - in full version would use session
    print(f"Flash {category}: {message}")


def get_flashed_messages(with_categories: bool = False, category_filter: Optional[list] = None):
    """Get flashed messages (Flask compatible)"""
    # Basic implementation - returns empty list
    return []


def send_file(filename: str, **kwargs):
    """Send file response (Flask compatible)"""
    # Basic implementation
    return GoFlaskResponse(
        data={"file": filename},
        headers={"Content-Type": "application/octet-stream"}
    )


def send_from_directory(directory: str, filename: str, **kwargs):
    """Send file from directory (Flask compatible)"""
    import os
    filepath = os.path.join(directory, filename)
    return send_file(filepath, **kwargs)


def render_template(template_name: str, **context):
    """Render template (Flask compatible - basic implementation)"""
    # Basic implementation - in full version would use Jinja2
    return GoFlaskResponse(
        data={
            "template": template_name,
            "context": context
        },
        headers={"Content-Type": "text/html"}
    )


def render_template_string(source: str, **context):
    """Render template from string (Flask compatible)"""
    # Basic implementation
    return GoFlaskResponse(
        data={
            "template_string": source,
            "context": context
        },
        headers={"Content-Type": "text/html"}
    )
