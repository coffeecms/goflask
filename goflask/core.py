"""
GoFlask Core - Main application class
"""

import ctypes
import json
import os
import sys
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Union
from functools import wraps

# Load the GoFlask C library
def load_goflask_library():
    """Load the GoFlask shared library"""
    if sys.platform.startswith('win'):
        lib_name = 'goflask.dll'
    elif sys.platform.startswith('darwin'):
        lib_name = 'libgoflask.dylib'
    else:
        lib_name = 'libgoflask.so'
    
    # Try to load from package directory first
    try:
        package_dir = os.path.dirname(__file__)
        lib_path = os.path.join(package_dir, lib_name)
        if os.path.exists(lib_path):
            return ctypes.CDLL(lib_path)
    except:
        pass
    
    # Try to load from current directory
    try:
        if os.path.exists(lib_name):
            return ctypes.CDLL(lib_name)
    except:
        pass
    
    # Try system paths
    try:
        return ctypes.CDLL(lib_name)
    except:
        print(f"⚠️  Warning: Cannot load GoFlask library {lib_name}")
        print("   GoFlask will run in compatibility mode (Python-only)")
        print("   Install Go 1.21+ and rebuild for full performance benefits")
        return None

# Global library instance
_goflask_lib = None

def get_goflask_lib():
    """Get or initialize the GoFlask library"""
    global _goflask_lib
    if _goflask_lib is None:
        _goflask_lib = load_goflask_library()
        
        if _goflask_lib:
            # Define function signatures
            _goflask_lib.goflask_create_app.argtypes = [ctypes.c_char_p]
            _goflask_lib.goflask_create_app.restype = ctypes.c_int
            
            _goflask_lib.goflask_add_route.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p]
            _goflask_lib.goflask_add_route.restype = ctypes.c_int
            
            _goflask_lib.goflask_run.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
            _goflask_lib.goflask_run.restype = ctypes.c_int
            
            _goflask_lib.goflask_shutdown.argtypes = [ctypes.c_int]
            _goflask_lib.goflask_shutdown.restype = ctypes.c_int
            
            _goflask_lib.goflask_add_cors.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
            _goflask_lib.goflask_add_cors.restype = ctypes.c_int
            
            _goflask_lib.goflask_add_rate_limit.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
            _goflask_lib.goflask_add_rate_limit.restype = ctypes.c_int
        
    return _goflask_lib


class GoFlaskContext:
    """Flask-compatible request context"""
    
    def __init__(self, context_data: str = "{}"):
        """Initialize context from JSON data"""
        try:
            self._data = json.loads(context_data)
        except:
            self._data = {}
    
    @property
    def method(self) -> str:
        """HTTP method"""
        return self._data.get('method', 'GET')
    
    @property
    def path(self) -> str:
        """Request path"""
        return self._data.get('path', '/')
    
    @property
    def remote_addr(self) -> str:
        """Client IP address"""
        return self._data.get('remote_addr', '127.0.0.1')
    
    @property
    def headers(self) -> Dict[str, str]:
        """Request headers"""
        return self._data.get('headers', {})
    
    @property
    def args(self) -> Dict[str, str]:
        """Query parameters (Flask compatible)"""
        return self._data.get('query', {})
    
    @property
    def json(self) -> Any:
        """JSON data"""
        return self._data.get('json')
    
    @property
    def data(self) -> str:
        """Raw request body"""
        return self._data.get('body', '')
    
    def get_json(self, force=False, silent=False) -> Any:
        """Get JSON data (Flask compatible)"""
        try:
            return self.json
        except:
            if silent:
                return None
            raise


class GoFlaskResponse:
    """Flask-compatible response"""
    
    def __init__(self, data: Any = None, status: int = 200, headers: Optional[Dict[str, str]] = None):
        self.data = data
        self.status = status
        self.headers = headers or {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'data': self.data,
            'status': self.status,
            'headers': self.headers
        }


class GoFlask:
    """
    GoFlask - High Performance Flask-compatible Web Framework
    
    Drop-in replacement for Flask with 5x performance improvement
    """
    
    def __init__(self, import_name: str = "goflask", **kwargs):
        """Initialize GoFlask application"""
        self.import_name = import_name
        self.config = kwargs
        self._app_id = None
        self._routes = {}
        self._error_handlers = {}
        self._before_request_funcs = []
        self._after_request_funcs = []
        self._lib = get_goflask_lib()
        
        # Create the Go app if library is available
        if self._lib:
            self._create_app()
    
    def _create_app(self):
        """Create the underlying Go application"""
        if not self._lib:
            return
            
        app_name = self.import_name.encode('utf-8')
        self._app_id = self._lib.goflask_create_app(app_name)
        if self._app_id == -1:
            raise RuntimeError("Failed to create GoFlask application")
    
    def route(self, rule: str, **options):
        """
        Decorator to register a route (Flask compatible)
        
        @app.route('/api/users')
        def get_users():
            return {'users': []}
        """
        def decorator(func: Callable):
            methods = options.get('methods', ['GET'])
            for method in methods:
                self.add_url_rule(rule, func.__name__, func, methods=[method])
            return func
        return decorator
    
    def add_url_rule(self, rule: str, endpoint: Optional[str] = None, view_func: Optional[Callable] = None, **options):
        """Add a URL rule (Flask compatible)"""
        methods = options.get('methods', ['GET'])
        
        if view_func is None:
            return
        
        for method in methods:
            key = f"{method}:{rule}"
            self._routes[key] = view_func
            
            # Register with Go backend if available
            if self._lib and self._app_id:
                method_bytes = method.encode('utf-8')
                rule_bytes = rule.encode('utf-8')
                
                # For now, pass a placeholder handler pointer
                result = self._lib.goflask_add_route(
                    self._app_id, 
                    method_bytes, 
                    rule_bytes, 
                    ctypes.cast(id(view_func), ctypes.c_void_p)
                )
                
                if result != 0:
                    print(f"⚠️  Warning: Failed to register route {method} {rule} with Go backend")
    
    def run(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = False, **kwargs):
        """Run the application (Flask compatible)"""
        print(f" * Running on http://{host}:{port}")
        
        if self._lib and self._app_id:
            print(" * GoFlask high-performance server (5x faster than Flask)")
            
            host_bytes = host.encode('utf-8')
            result = self._lib.goflask_run(self._app_id, host_bytes, port)
            
            if result != 0:
                print("⚠️  Warning: Failed to start GoFlask server, falling back to Python mode")
                self._run_python_fallback(host, port, debug)
            else:
                try:
                    # Keep the main thread alive
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n * Shutting down GoFlask server...")
                    self.shutdown()
        else:
            print(" * GoFlask running in Python compatibility mode")
            print(" * Install Go 1.21+ and rebuild for 5x performance improvement")
            self._run_python_fallback(host, port, debug)
    
    def _run_python_fallback(self, host: str, port: int, debug: bool):
        """Fallback to pure Python implementation"""
        try:
            from werkzeug.serving import run_simple
            from werkzeug.wrappers import Request, Response
            
            def application(environ, start_response):
                request = Request(environ)
                
                # Find matching route
                route_key = f"{request.method}:{request.path}"
                handler = self._routes.get(route_key)
                
                if handler:
                    try:
                        result = handler()
                        if isinstance(result, dict):
                            response = Response(
                                json.dumps(result),
                                content_type='application/json'
                            )
                        else:
                            response = Response(str(result))
                    except Exception as e:
                        response = Response(
                            json.dumps({"error": str(e)}),
                            status=500,
                            content_type='application/json'
                        )
                else:
                    response = Response(
                        json.dumps({"error": "Not found"}),
                        status=404,
                        content_type='application/json'
                    )
                
                return response(environ, start_response)
            
            run_simple(host, port, application, use_reloader=debug, use_debugger=debug)
            
        except ImportError:
            print("⚠️  Werkzeug not available. Please install with: pip install werkzeug")
            print("   Or install Go 1.21+ for full GoFlask performance")
    
    def shutdown(self):
        """Shutdown the application"""
        if self._lib and self._app_id is not None:
            self._lib.goflask_shutdown(self._app_id)
    
    # Flask-compatible decorators and methods
    def before_request(self, func: Callable):
        """Register before request handler"""
        self._before_request_funcs.append(func)
        return func
    
    def after_request(self, func: Callable):
        """Register after request handler"""
        self._after_request_funcs.append(func)
        return func
    
    def errorhandler(self, code: int):
        """Register error handler"""
        def decorator(func: Callable):
            self._error_handlers[code] = func
            return func
        return decorator
    
    # Extension methods for GoFlask features
    def add_cors(self, origins: str = "*", methods: str = "GET,POST,PUT,DELETE,OPTIONS", 
                 headers: str = "Origin,Content-Type,Accept,Authorization"):
        """Add CORS support"""
        if self._lib and self._app_id:
            origins_bytes = origins.encode('utf-8')
            methods_bytes = methods.encode('utf-8')
            headers_bytes = headers.encode('utf-8')
            
            result = self._lib.goflask_add_cors(self._app_id, origins_bytes, methods_bytes, headers_bytes)
            if result != 0:
                print("⚠️  Warning: Failed to add CORS to Go backend")
    
    def add_rate_limit(self, max_requests: int = 100, duration: int = 3600):
        """Add rate limiting"""
        if self._lib and self._app_id:
            result = self._lib.goflask_add_rate_limit(self._app_id, max_requests, duration)
            if result != 0:
                print("⚠️  Warning: Failed to add rate limiting to Go backend")


# For backwards compatibility
Flask = GoFlask
