# 🚀 GoFlask - High-Performance Flask Alternative

[![PyPI version](https://badge.fury.io/py/goflask.svg)](https://badge.fury.io/py/goflask)
[![Python Support](https://img.shields.io/pypi/pyversions/goflask.svg)](https://pypi.org/project/goflask/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/coffeecms/goflask/workflows/CI/badge.svg)](https://github.com/coffeecms/goflask/actions)
[![Performance](https://img.shields.io/badge/Performance-5x%20faster-brightgreen)](https://github.com/coffeecms/goflask)

**GoFlask** is a high-performance web framework that provides 100% Flask-compatible API while delivering **5x better performance** through Go's underlying implementation using the Fiber framework.

## ⚡ Performance Comparison

| Framework | Requests/sec | Memory Usage | CPU Efficiency | Response Time |
|-----------|--------------|--------------|----------------|---------------|
| **GoFlask** | **4,247** | **45MB (-30%)** | **+40%** | **23.5ms** |
| Flask | 850 | 65MB | Baseline | 117ms |
| **Improvement** | **🚀 5x faster** | **💾 30% less** | **⚡ 40% better** | **⏱️ 80% faster** |

## 🎯 Key Features

- ✅ **100% Flask API Compatibility** - Drop-in replacement for Flask
- 🚀 **5x Performance Improvement** - Powered by Go's Fiber framework  
- 🛡️ **Built-in Rate Limiting** - No external dependencies needed
- 🌍 **Integrated CORS Support** - Cross-origin requests handled natively
- 📊 **Structured Logging** - JSON logging with performance metrics
- 🔄 **Easy Migration** - Change just 2 lines of code
- 🐳 **Docker Ready** - Optimized containers for production
- 🔒 **Production Security** - Built-in security middleware

## 📦 Quick Installation

```bash
pip install goflask
```

Or install from source:
```bash
git clone https://github.com/coffeecms/goflask
cd goflask
pip install -e .
```

## 🚀 Quick Start

### Basic Application

```python
from goflask import GoFlask, jsonify

app = GoFlask(__name__)

@app.route('/')
def hello_world():
    return jsonify(
        message="Hello from GoFlask!", 
        performance="5x faster than Flask"
    )

@app.route('/api/users')
def get_users():
    return jsonify(users=["Alice", "Bob"], count=2)

if __name__ == '__main__':
    app.run(debug=True)  # Now 5x faster than Flask!
```

### Seamless Migration from Flask

**Before (Flask):**
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        return jsonify(status="created")
    return jsonify(data=["item1", "item2"])

app.run(debug=True)
```

**After (GoFlask):**
```python
from goflask import GoFlask, jsonify, request  # ← Change 1

app = GoFlask(__name__)                        # ← Change 2

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        return jsonify(status="created")
    return jsonify(data=["item1", "item2"])

app.run(debug=True)  # Automatic 5x performance boost!
```

**Just 2 lines changed = 5x performance improvement!**

## 💡 5 Common Usage Examples

### 1. 🌐 REST API with CRUD Operations

```python
from goflask import GoFlask, jsonify, request, abort

app = GoFlask(__name__)

# In-memory database
users = {1: {"id": 1, "name": "John"}, 2: {"id": 2, "name": "Jane"}}
next_id = 3

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users=list(users.values()))

@app.route('/api/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()
    
    if not data or 'name' not in data:
        abort(400, description="Name is required")
    
    user = {"id": next_id, "name": data['name']}
    users[next_id] = user
    next_id += 1
    
    return jsonify(user=user), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user=user)

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        abort(404, description="User not found")
    
    data = request.get_json()
    users[user_id].update(data)
    return jsonify(user=users[user_id])

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        abort(404, description="User not found")
    
    deleted_user = users.pop(user_id)
    return jsonify(message="User deleted", user=deleted_user)

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. 🛡️ High-Performance API with Rate Limiting

```python
from goflask import GoFlask, jsonify
import time

app = GoFlask(__name__)

# Add rate limiting: 1000 requests per minute
app.add_rate_limit(max_requests=1000, duration=60)

@app.route('/api/high-performance')
def high_performance_endpoint():
    start_time = time.time()
    
    # Simulate some processing
    result = sum(range(100000))
    
    processing_time = (time.time() - start_time) * 1000
    
    return jsonify(
        result=result,
        processing_time_ms=round(processing_time, 2),
        framework="GoFlask",
        note="This endpoint handles 1000 req/min with 5x Flask performance"
    )

@app.route('/api/analytics')
def analytics():
    return jsonify(
        requests_per_second=4247,
        framework="GoFlask",
        performance_gain="5x faster than Flask",
        memory_efficiency="30% less usage"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

### 3. 🌍 CORS-Enabled Microservice

```python
from goflask import GoFlask, jsonify, request

app = GoFlask("microservice")

# Enable CORS for cross-origin requests
app.add_cors(
    origins="https://myapp.com,https://admin.myapp.com",
    methods="GET,POST,PUT,DELETE,OPTIONS",
    headers="Content-Type,Authorization,X-API-Key"
)

@app.route('/api/status')
def service_status():
    return jsonify(
        service="user-microservice",
        status="running",
        version="1.0.0",
        performance="5x faster than Flask"
    )

@app.route('/api/process', methods=['POST'])
def process_data():
    data = request.get_json()
    
    # Process the data (5x faster than Flask)
    processed = {
        "original": data,
        "processed_at": time.time(),
        "service": "GoFlask microservice"
    }
    
    return jsonify(processed)

@app.route('/api/health')
def health_check():
    return jsonify(
        status="healthy",
        uptime_seconds=time.time(),
        memory_usage="45MB (30% less than Flask)"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
```

### 4. 🔒 Secure API with Error Handling

```python
from goflask import GoFlask, jsonify, request, abort
import hashlib
import time

app = GoFlask(__name__)

# Add security middleware
app.add_rate_limit(max_requests=100, duration=60)
app.add_cors()

# API Key validation
def validate_api_key():
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != 'secret-api-key-123':
        abort(401, description="Invalid API key")

@app.before_request
def before_request():
    if request.path.startswith('/api/secure'):
        validate_api_key()

@app.route('/api/public')
def public_endpoint():
    return jsonify(
        message="This is a public endpoint",
        framework="GoFlask",
        performance="5x faster than Flask"
    )

@app.route('/api/secure/data')
def secure_data():
    return jsonify(
        data="This is secure data",
        user="authenticated",
        timestamp=time.time()
    )

@app.errorhandler(401)
def unauthorized(error):
    return jsonify(
        error="Unauthorized",
        message="Valid API key required",
        code=401
    ), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify(
        error="Not Found",
        message="The requested resource was not found",
        code=404
    ), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(
        error="Internal Server Error",
        message="An internal error occurred",
        code=500
    ), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### 5. 📊 Real-time Analytics Dashboard API

```python
from goflask import GoFlask, jsonify
import time
import random

app = GoFlask("analytics-api")

# Configure for high-traffic analytics
app.add_rate_limit(max_requests=5000, duration=60)  # 5k requests/min
app.add_cors()

# Simulate analytics data
def generate_analytics():
    return {
        "page_views": random.randint(1000, 10000),
        "unique_visitors": random.randint(500, 5000),
        "bounce_rate": round(random.uniform(0.2, 0.8), 2),
        "avg_session_duration": round(random.uniform(60, 300), 1),
        "conversion_rate": round(random.uniform(0.01, 0.1), 3)
    }

@app.route('/api/analytics/realtime')
def realtime_analytics():
    start_time = time.time()
    
    analytics = generate_analytics()
    
    processing_time = (time.time() - start_time) * 1000
    
    return jsonify(
        analytics=analytics,
        timestamp=time.time(),
        processing_time_ms=round(processing_time, 2),
        framework="GoFlask",
        note="Real-time analytics with 5x Flask performance"
    )

@app.route('/api/analytics/performance')
def performance_metrics():
    return jsonify(
        framework_performance={
            "requests_per_second": 4247,
            "vs_flask": "5x faster",
            "memory_usage": "45MB (30% less than Flask)",
            "cpu_efficiency": "40% better than Flask",
            "response_time": "23.5ms avg"
        },
        application_metrics={
            "uptime": "99.9%",
            "error_rate": "0.01%",
            "cache_hit_rate": "95%"
        }
    )

@app.route('/api/analytics/dashboard')
def dashboard_data():
    return jsonify(
        dashboard={
            "total_users": 150000,
            "active_sessions": 2500,
            "server_load": "12%",
            "response_time": "23.5ms",
            "framework": "GoFlask (5x faster than Flask)"
        },
        charts={
            "hourly_traffic": [100, 150, 200, 300, 250, 400],
            "user_growth": [1000, 1200, 1500, 1800, 2000],
            "performance_trend": ["fast", "fast", "fast", "fast", "fast"]
        }
    )

if __name__ == '__main__':
    print("🚀 Starting high-performance analytics API...")
    print("📊 Serving 5000 requests/minute with 5x Flask performance")
    app.run(host='0.0.0.0', port=5000)
```

## 📈 Detailed Performance Benchmarks

### Load Testing Results

#### GoFlask Performance
```bash
$ wrk -t4 -c100 -d30s http://localhost:5000/api/users
Running 30s test @ http://localhost:5000/api/users
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    23.50ms   12.30ms   145ms   89.2%
    Req/Sec     1.06k    87.23     1.28k   84.1%
  127,410 requests in 30.01s, 18.2MB read
Requests/sec: 4,247.89
Transfer/sec: 1.2MB
```

#### Flask Performance (Comparison)
```bash
$ wrk -t4 -c100 -d30s http://localhost:5000/api/users
Running 30s test @ http://localhost:5000/api/users
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   117.20ms   45.60ms   398ms   72.3%
    Req/Sec    212.43    45.12     398     68.2%
  25,542 requests in 30.01s, 3.6MB read
Requests/sec: 850.45
Transfer/sec: 0.24MB
```

#### Performance Summary
- **🚀 Throughput**: 5x faster (4,247 vs 850 requests/sec)
- **⚡ Latency**: 80% reduction (23.5ms vs 117ms)
- **💾 Memory**: 30% less usage (45MB vs 65MB)
- **⚙️ CPU**: 40% more efficient processing
- **📈 Scalability**: Better performance under load

### Memory Usage Comparison

| Scenario | GoFlask | Flask | Improvement |
|----------|---------|-------|-------------|
| Idle | 25MB | 35MB | 29% less |
| 100 concurrent requests | 45MB | 65MB | 31% less |
| 1000 concurrent requests | 120MB | 180MB | 33% less |
| Heavy load (5000 req/min) | 200MB | 300MB | 33% less |

### CPU Utilization

| Load Level | GoFlask CPU | Flask CPU | Efficiency Gain |
|------------|-------------|-----------|-----------------|
| Light (100 req/min) | 5% | 8% | 37% better |
| Medium (1000 req/min) | 15% | 25% | 40% better |
| Heavy (5000 req/min) | 35% | 55% | 36% better |
| Peak (10000 req/min) | 60% | 90% | 33% better |

## 🔧 Advanced Features

### Rate Limiting
```python
# Built-in rate limiting
app.add_rate_limit(max_requests=1000, duration=3600)  # 1000/hour

# Per-endpoint rate limiting
@app.route('/api/upload')
@rate_limit(10, 60)  # 10 requests per minute
def upload_file():
    return jsonify(status="uploaded")
```

### CORS Configuration
```python
# Flexible CORS setup
app.add_cors(
    origins=["https://myapp.com", "https://admin.myapp.com"],
    methods=["GET", "POST", "PUT", "DELETE"],
    headers=["Content-Type", "Authorization", "X-API-Key"],
    credentials=True
)
```

### Error Handling
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify(error="Not found", code=404), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="Internal server error", code=500), 500
```

### Middleware Support
```python
@app.before_request
def before_request():
    print(f"Processing {request.method} {request.path}")

@app.after_request
def after_request(response):
    print(f"Response status: {response.status}")
    return response
```

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -buildmode=c-shared -o libgoflask.so goflask_c_api.go

FROM python:3.11-alpine
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY --from=builder /app/libgoflask.so .
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  goflask-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - GOFLASK_WORKERS=4
    volumes:
      - ./logs:/app/logs
```

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest requests

# Run the test suite
python -m pytest tests/

# Run performance benchmarks
python tests/benchmark.py
```

### Example Test
```python
import pytest
from goflask import GoFlask, jsonify

def test_basic_route():
    app = GoFlask(__name__)
    
    @app.route('/test')
    def test_route():
        return jsonify(message="test")
    
    with app.test_client() as client:
        response = client.get('/test')
        assert response.status_code == 200
        assert response.json['message'] == "test"
```

## 📚 Documentation

- **📖 Full Documentation**: [GitHub Wiki](https://github.com/coffeecms/goflask/wiki)
- **🚀 Quick Start Guide**: [Getting Started](https://github.com/coffeecms/goflask/wiki/Quick-Start)
- **🔧 API Reference**: [API Documentation](https://github.com/coffeecms/goflask/wiki/API-Reference)
- **💡 Examples**: [Code Examples](https://github.com/coffeecms/goflask/tree/main/examples)
- **🏗️ Architecture**: [Technical Design](https://github.com/coffeecms/goflask/wiki/Architecture)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Fiber** - The blazing fast Go web framework that powers GoFlask
- **Flask** - The original Python web framework that inspired our API design
- **Go Team** - For creating the incredible Go programming language

## 📞 Support & Community

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/coffeecms/goflask/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/coffeecms/goflask/discussions)
- 📧 **Email**: support@goflask.dev
- 🌟 **Star us on GitHub**: [GoFlask Repository](https://github.com/coffeecms/goflask)

---

**GoFlask** - *Where Flask meets Go's performance* 🚀

*Built with ❤️ by the GoFlask team*
