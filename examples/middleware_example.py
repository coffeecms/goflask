"""
Middleware Example - Using CORS and Rate Limiting
"""

from goflask import GoFlask, jsonify, request

# Create application instance
app = GoFlask(__name__)

# Enable CORS middleware for cross-origin requests
app.enable_cors(
    origins=['http://localhost:3000', 'https://myapp.com'],
    methods=['GET', 'POST', 'PUT', 'DELETE'],
    headers=['Content-Type', 'Authorization']
)

# Enable rate limiting middleware
app.enable_rate_limiting(
    max_requests=100,  # 100 requests
    window_seconds=60,  # per minute
    storage='memory'   # use memory storage
)

# Basic routes
@app.route('/')
def index():
    return jsonify({
        'message': 'GoFlask with CORS and Rate Limiting',
        'features': ['CORS enabled', 'Rate limiting active']
    })

@app.route('/api/public')
def public_endpoint():
    """Public endpoint accessible from any origin"""
    return jsonify({
        'data': 'This is public data',
        'timestamp': '2024-01-01T00:00:00Z'
    })

@app.route('/api/protected', methods=['POST'])
def protected_endpoint():
    """Protected endpoint with rate limiting"""
    data = request.json or {}
    
    return jsonify({
        'message': 'Protected data processed',
        'received': data,
        'status': 'success'
    })

@app.route('/api/upload', methods=['POST'])
def upload_endpoint():
    """File upload endpoint with CORS support"""
    # Check if file was uploaded
    files = getattr(request, 'files', {})
    
    if not files:
        return jsonify({
            'error': 'No file uploaded'
        }), 400
    
    return jsonify({
        'message': 'File uploaded successfully',
        'files': list(files.keys())
    })

@app.route('/api/bulk', methods=['POST'])
def bulk_endpoint():
    """Bulk operation endpoint that might hit rate limits"""
    data = request.json or {}
    items = data.get('items', [])
    
    # Simulate bulk processing
    processed = []
    for item in items[:10]:  # Limit to 10 items
        processed.append({
            'id': item.get('id'),
            'status': 'processed'
        })
    
    return jsonify({
        'message': f'Processed {len(processed)} items',
        'results': processed
    })

# Custom CORS configuration for specific endpoint
@app.route('/api/custom-cors')
def custom_cors():
    """Endpoint with custom CORS headers"""
    response = jsonify({
        'message': 'Custom CORS endpoint',
        'cors': 'custom headers applied'
    })
    
    # Add custom headers (this would be handled by Go backend)
    return response

# Rate limit status endpoint
@app.route('/api/rate-limit-status')
def rate_limit_status():
    """Check current rate limit status"""
    # In a real implementation, this would check the current rate limit status
    return jsonify({
        'rate_limit': {
            'remaining': 95,
            'reset_time': '2024-01-01T00:01:00Z',
            'limit': 100
        }
    })

# Error handlers
@app.errorhandler(429)
def rate_limit_exceeded(error):
    """Handle rate limit exceeded errors"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again later.',
        'retry_after': 60
    }), 429

@app.errorhandler(403)
def cors_error(error):
    """Handle CORS errors"""
    return jsonify({
        'error': 'CORS error',
        'message': 'Cross-origin request not allowed'
    }), 403

# Middleware configuration examples
def configure_advanced_cors():
    """Example of advanced CORS configuration"""
    app.enable_cors(
        origins=['*'],  # Allow all origins (not recommended for production)
        methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
        headers=['*'],  # Allow all headers
        credentials=True,  # Allow credentials
        max_age=86400  # Cache preflight for 24 hours
    )

def configure_redis_rate_limiting():
    """Example of Redis-based rate limiting"""
    app.enable_rate_limiting(
        max_requests=1000,  # 1000 requests
        window_seconds=3600,  # per hour
        storage='redis',
        redis_url='redis://localhost:6379'
    )

if __name__ == '__main__':
    # You can uncomment these for advanced configurations
    # configure_advanced_cors()
    # configure_redis_rate_limiting()
    
    print("Starting GoFlask server with CORS and Rate Limiting...")
    print("CORS origins:", ['http://localhost:3000', 'https://myapp.com'])
    print("Rate limit: 100 requests per minute")
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)
