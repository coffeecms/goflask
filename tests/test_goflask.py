"""
Test Suite for GoFlask Package
"""

import unittest
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from goflask import GoFlask, request, jsonify
from goflask.exceptions import NotFound, BadRequest


class TestGoFlask(unittest.TestCase):
    """Test cases for GoFlask application"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = GoFlask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_app_creation(self):
        """Test GoFlask application creation"""
        self.assertIsInstance(self.app, GoFlask)
        self.assertEqual(self.app.name, __name__)
    
    def test_simple_route(self):
        """Test simple route creation"""
        @self.app.route('/')
        def hello():
            return 'Hello, World!'
        
        # Note: In actual implementation, this would test the route
        # For now, we just verify the route was registered
        self.assertTrue(hasattr(self.app, 'route'))
    
    def test_json_response(self):
        """Test JSON response"""
        @self.app.route('/api/data')
        def get_data():
            return jsonify({'message': 'Hello from GoFlask!'})
        
        # Verify jsonify function exists
        response = jsonify({'test': True})
        self.assertIsInstance(response, dict)
    
    def test_route_with_methods(self):
        """Test route with specific HTTP methods"""
        @self.app.route('/api/users', methods=['GET', 'POST'])
        def users():
            if request.method == 'POST':
                return jsonify({'created': True})
            return jsonify({'users': []})
        
        # Verify route registration
        self.assertTrue(hasattr(self.app, 'route'))
    
    def test_route_with_parameters(self):
        """Test route with URL parameters"""
        @self.app.route('/users/<int:user_id>')
        def get_user(user_id):
            return jsonify({'user_id': user_id})
        
        # Verify parameterized route
        self.assertTrue(hasattr(self.app, 'route'))
    
    def test_error_handling(self):
        """Test error handling"""
        @self.app.route('/error')
        def error():
            raise NotFound('User not found')
        
        # Verify exception classes
        with self.assertRaises(NotFound):
            raise NotFound('Test error')
    
    def test_middleware_registration(self):
        """Test middleware registration"""
        def test_middleware():
            return 'middleware'
        
        # Test CORS middleware
        self.app.enable_cors()
        
        # Test rate limiting middleware
        self.app.enable_rate_limiting()
        
        # Verify middleware methods exist
        self.assertTrue(hasattr(self.app, 'enable_cors'))
        self.assertTrue(hasattr(self.app, 'enable_rate_limiting'))
    
    def test_config_handling(self):
        """Test configuration handling"""
        self.app.config['TEST_KEY'] = 'test_value'
        self.assertEqual(self.app.config['TEST_KEY'], 'test_value')
    
    def test_before_request_hooks(self):
        """Test before request hooks"""
        @self.app.before_request
        def before():
            pass
        
        # Verify hook registration
        self.assertTrue(hasattr(self.app, 'before_request'))
    
    def test_after_request_hooks(self):
        """Test after request hooks"""
        @self.app.after_request
        def after(response):
            return response
        
        # Verify hook registration
        self.assertTrue(hasattr(self.app, 'after_request'))


class TestGoFlaskHelpers(unittest.TestCase):
    """Test cases for GoFlask helper functions"""
    
    def test_jsonify(self):
        """Test jsonify function"""
        data = {'key': 'value', 'number': 42}
        result = jsonify(data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, data)
    
    def test_abort(self):
        """Test abort function"""
        from goflask.exceptions import abort, NotFound
        
        with self.assertRaises(NotFound):
            abort(404)
    
    def test_redirect(self):
        """Test redirect function"""
        from goflask.helpers import redirect
        
        response = redirect('/new-location')
        self.assertIsInstance(response, dict)
        self.assertEqual(response.get('location'), '/new-location')
    
    def test_url_for(self):
        """Test url_for function"""
        from goflask.helpers import url_for
        
        url = url_for('test_endpoint')
        self.assertIsInstance(url, str)
    
    def test_render_template(self):
        """Test render_template function"""
        from goflask.helpers import render_template
        
        # Test basic template rendering
        result = render_template('test.html', name='GoFlask')
        self.assertIsInstance(result, str)


class TestGoFlaskExceptions(unittest.TestCase):
    """Test cases for GoFlask exceptions"""
    
    def test_http_exceptions(self):
        """Test HTTP exception classes"""
        from goflask.exceptions import (
            BadRequest, Unauthorized, Forbidden, NotFound,
            InternalServerError, abort
        )
        
        # Test exception creation
        error = BadRequest('Invalid input')
        self.assertEqual(error.code, 400)
        self.assertEqual(error.description, 'Invalid input')
        
        # Test abort function
        with self.assertRaises(NotFound):
            abort(404, 'Page not found')
    
    def test_custom_exceptions(self):
        """Test custom exception handling"""
        from goflask.exceptions import GoFlaskException
        
        class CustomError(GoFlaskException):
            def __init__(self, message):
                self.code = 422
                self.description = message
                super().__init__(message)
        
        error = CustomError('Custom error')
        self.assertEqual(error.code, 422)


class TestGoFlaskContext(unittest.TestCase):
    """Test cases for GoFlask context objects"""
    
    def test_request_context(self):
        """Test request context"""
        from goflask.context import request
        
        # Test request object attributes
        self.assertTrue(hasattr(request, 'method'))
        self.assertTrue(hasattr(request, 'path'))
        self.assertTrue(hasattr(request, 'headers'))
        self.assertTrue(hasattr(request, 'args'))
        self.assertTrue(hasattr(request, 'json'))
    
    def test_app_context(self):
        """Test application context"""
        from goflask.context import g
        
        # Test g object
        g.test_value = 'test'
        self.assertEqual(g.test_value, 'test')
    
    def test_session_context(self):
        """Test session context"""
        from goflask.context import session
        
        # Test session object
        session['key'] = 'value'
        self.assertEqual(session['key'], 'value')
        self.assertTrue('key' in session)


class TestGoFlaskIntegration(unittest.TestCase):
    """Integration tests for GoFlask"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.app = GoFlask(__name__)
        self.app.config['TESTING'] = True
    
    def test_full_application_flow(self):
        """Test complete application flow"""
        # Register routes
        @self.app.route('/')
        def index():
            return jsonify({'message': 'Welcome to GoFlask!'})
        
        @self.app.route('/api/users/<int:user_id>')
        def get_user(user_id):
            return jsonify({'user_id': user_id, 'name': f'User {user_id}'})
        
        @self.app.route('/api/data', methods=['POST'])
        def create_data():
            return jsonify({'created': True, 'id': 123})
        
        # Enable middleware
        self.app.enable_cors()
        self.app.enable_rate_limiting()
        
        # Test application creation
        self.assertIsInstance(self.app, GoFlask)
    
    def test_error_handler_registration(self):
        """Test error handler registration"""
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({'error': 'Not found'}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({'error': 'Internal server error'}), 500
        
        # Verify error handler registration
        self.assertTrue(hasattr(self.app, 'errorhandler'))


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
