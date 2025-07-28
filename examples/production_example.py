"""
Production Example - GoFlask in Production Environment
"""

import os
import logging
from goflask import GoFlask, jsonify, request
from goflask.exceptions import NotFound, BadRequest, InternalServerError

# Create application instance with production configuration
app = GoFlask(__name__)

# Production configuration
app.config.update({
    'DEBUG': False,
    'TESTING': False,
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'production-secret-key'),
    'DATABASE_URL': os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost/prod'),
    'REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379'),
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max file size
})

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler('/var/log/goflask/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Production middleware configuration
def configure_production_middleware():
    """Configure middleware for production use"""
    
    # CORS configuration for production
    app.enable_cors(
        origins=[
            'https://myapp.com',
            'https://www.myapp.com',
            'https://api.myapp.com'
        ],
        methods=['GET', 'POST', 'PUT', 'DELETE'],
        headers=['Content-Type', 'Authorization', 'X-API-Key'],
        credentials=True,
        max_age=3600  # Cache preflight for 1 hour
    )
    
    # Rate limiting with Redis for production
    app.enable_rate_limiting(
        max_requests=1000,  # 1000 requests
        window_seconds=3600,  # per hour
        storage='redis',
        redis_url=app.config['REDIS_URL'],
        key_prefix='rate_limit:',
        headers=True  # Include rate limit headers in response
    )
    
    # Additional security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

# Health check endpoints
@app.route('/health')
def health_check():
    """Health check endpoint for load balancers"""
    return jsonify({
        'status': 'healthy',
        'timestamp': '2024-01-01T00:00:00Z',
        'version': '1.0.0'
    })

@app.route('/health/ready')
def readiness_check():
    """Readiness check for Kubernetes"""
    # Check database connection, Redis, etc.
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'external_api': check_external_api()
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return jsonify({
        'status': 'ready' if all_healthy else 'not_ready',
        'checks': checks
    }), status_code

@app.route('/health/live')
def liveness_check():
    """Liveness check for Kubernetes"""
    return jsonify({'status': 'alive'}), 200

# API endpoints with production features
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """Get users with pagination and filtering"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)  # Max 100 per page
        search = request.args.get('search', '')
        
        # Simulate database query with pagination
        # In production, use actual database with proper queries
        total_users = 1000
        start = (page - 1) * per_page
        end = start + per_page
        
        users = [
            {
                'id': i,
                'username': f'user_{i}',
                'email': f'user_{i}@example.com',
                'created_at': '2024-01-01T00:00:00Z'
            }
            for i in range(start + 1, min(end + 1, total_users + 1))
            if not search or search.lower() in f'user_{i}'
        ]
        
        return jsonify({
            'users': users,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_users,
                'pages': (total_users + per_page - 1) // per_page
            }
        })
    
    except Exception as e:
        logger.error(f"Error in get_users: {str(e)}")
        raise InternalServerError('Failed to fetch users')

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user with caching"""
    try:
        # In production, check cache first
        cache_key = f'user:{user_id}'
        
        # Simulate user lookup
        if user_id <= 0 or user_id > 1000:
            raise NotFound(f'User {user_id} not found')
        
        user = {
            'id': user_id,
            'username': f'user_{user_id}',
            'email': f'user_{user_id}@example.com',
            'profile': {
                'first_name': f'User',
                'last_name': f'{user_id}',
                'bio': f'Biography for user {user_id}'
            },
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z'
        }
        
        return jsonify(user)
    
    except NotFound:
        raise
    except Exception as e:
        logger.error(f"Error in get_user {user_id}: {str(e)}")
        raise InternalServerError('Failed to fetch user')

@app.route('/api/v1/analytics', methods=['POST'])
def track_analytics():
    """Analytics endpoint with validation"""
    try:
        data = request.json
        
        if not data:
            raise BadRequest('No data provided')
        
        required_fields = ['event', 'user_id', 'timestamp']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise BadRequest(f'Missing required fields: {", ".join(missing_fields)}')
        
        # In production, send to analytics service
        logger.info(f"Analytics event: {data['event']} from user {data['user_id']}")
        
        return jsonify({
            'status': 'recorded',
            'event_id': f'evt_{data["user_id"]}_{data["timestamp"]}'
        }), 201
    
    except (BadRequest, NotFound):
        raise
    except Exception as e:
        logger.error(f"Error in track_analytics: {str(e)}")
        raise InternalServerError('Failed to record analytics')

# Helper functions for health checks
def check_database():
    """Check database connectivity"""
    try:
        # In production, actually check database
        return True
    except:
        return False

def check_redis():
    """Check Redis connectivity"""
    try:
        # In production, actually check Redis
        return True
    except:
        return False

def check_external_api():
    """Check external API connectivity"""
    try:
        # In production, check external services
        return True
    except:
        return False

# Error handlers with production logging
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.path}")
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(400)
def bad_request(error):
    logger.warning(f"400 error: {request.path} - {str(error)}")
    return jsonify({
        'error': 'Bad request',
        'message': str(error)
    }), 400

@app.errorhandler(429)
def rate_limit_exceeded(error):
    logger.warning(f"Rate limit exceeded: {request.remote_addr}")
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again later.'
    }), 429

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {request.path} - {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

# Request logging middleware
@app.before_request
def log_request():
    """Log incoming requests"""
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")

@app.after_request
def log_response(response):
    """Log response status"""
    logger.info(f"Response {response.status_code} for {request.method} {request.path}")
    return response

if __name__ == '__main__':
    # Configure production middleware
    configure_production_middleware()
    
    # Production server configuration
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    workers = int(os.environ.get('WORKERS', 4))
    
    logger.info(f"Starting GoFlask production server on {host}:{port}")
    logger.info(f"Configuration: {workers} workers, Redis caching, CORS enabled")
    
    # In production, use a proper WSGI server like Gunicorn
    # gunicorn -w 4 -b 0.0.0.0:8080 production_example:app
    app.run(
        host=host,
        port=port,
        debug=False,
        workers=workers
    )
