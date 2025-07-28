"""
GoFlask Context - Request context and global objects
"""

from typing import Any, Dict, Optional
from .core import GoFlaskContext


class _RequestContext:
    """Request context for Flask compatibility"""
    
    def __init__(self):
        self.method = 'GET'
        self.path = '/'
        self.headers = {}
        self.args = {}
        self.json = None
        self.data = ''
        self.remote_addr = '127.0.0.1'
        self.form = {}
        self.files = {}
        self.cookies = {}
        self.url = 'http://localhost:5000/'
        self.base_url = 'http://localhost:5000/'
        self.url_root = 'http://localhost:5000/'
    
    def get_json(self, force: bool = False, silent: bool = False) -> Any:
        """Get JSON data (Flask compatible)"""
        try:
            return self.json
        except:
            if silent:
                return None
            raise


class _AppContext:
    """Application context for Flask compatibility"""
    
    def __init__(self):
        self._data = {}
    
    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)
    
    def __setattr__(self, name: str, value: Any):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            if not hasattr(self, '_data'):
                super().__setattr__('_data', {})
            self._data[name] = value


class _SessionContext:
    """Session context for Flask compatibility"""
    
    def __init__(self):
        self._data = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        return self._data[key]
    
    def __setitem__(self, key: str, value: Any):
        self._data[key] = value
    
    def __delitem__(self, key: str):
        del self._data[key]
    
    def __contains__(self, key: str) -> bool:
        return key in self._data
    
    def pop(self, key: str, default: Any = None) -> Any:
        return self._data.pop(key, default)
    
    def setdefault(self, key: str, value: Any) -> Any:
        return self._data.setdefault(key, value)
    
    def clear(self):
        self._data.clear()
    
    def keys(self):
        return self._data.keys()
    
    def values(self):
        return self._data.values()
    
    def items(self):
        return self._data.items()


# Global context objects for Flask compatibility
request = _RequestContext()
g = _AppContext()
session = _SessionContext()


def has_request_context() -> bool:
    """Check if we're in a request context"""
    return True  # Simplified implementation


def has_app_context() -> bool:
    """Check if we're in an app context"""
    return True  # Simplified implementation


def copy_current_request_context(f):
    """Copy current request context (decorator)"""
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper


class LocalProxy:
    """Local proxy for Flask compatibility"""
    
    def __init__(self, local, name=None):
        self._local = local
        self._name = name
    
    def __getattr__(self, name):
        return getattr(self._local, name)
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            setattr(self._local, name, value)
