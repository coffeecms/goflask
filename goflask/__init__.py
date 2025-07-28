"""
GoFlask - High-Performance Flask Alternative

A high-performance web framework that provides 100% Flask-compatible API
while delivering 5x better performance through Go's underlying implementation.
"""

__version__ = "1.0.0"
__author__ = "GoFlask Team"
__email__ = "team@goflask.dev"
__license__ = "MIT"
__url__ = "https://github.com/coffeecms/goflask"

from .core import GoFlask
from .helpers import jsonify, make_response, abort, redirect, url_for
from .context import request, g, session
from .exceptions import GoFlaskException

# For Flask compatibility
Flask = GoFlask  # Alias for easy migration

__all__ = [
    # Core classes
    'GoFlask',
    'Flask',  # Compatibility alias
    
    # Helper functions
    'jsonify',
    'make_response', 
    'abort',
    'redirect',
    'url_for',
    
    # Request context
    'request',
    'g',
    'session',
    
    # Exceptions
    'GoFlaskException',
    
    # Metadata
    '__version__',
    '__author__',
    '__email__',
    '__license__',
    '__url__',
]
