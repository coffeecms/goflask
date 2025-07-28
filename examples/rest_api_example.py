"""
REST API Example - Building a REST API with GoFlask
"""

from goflask import GoFlask, jsonify, request
from goflask.exceptions import NotFound, BadRequest

# Create application instance
app = GoFlask(__name__)

# In-memory data store (use database in production)
users = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
]
posts = [
    {'id': 1, 'title': 'First Post', 'content': 'Hello World!', 'user_id': 1},
    {'id': 2, 'title': 'Second Post', 'content': 'GoFlask is awesome!', 'user_id': 2}
]

# Helper functions
def find_user(user_id):
    return next((user for user in users if user['id'] == user_id), None)

def find_post(post_id):
    return next((post for post in posts if post['id'] == post_id), None)

# User endpoints
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({
        'users': users,
        'total': len(users)
    })

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = find_user(user_id)
    if not user:
        raise NotFound(f'User {user_id} not found')
    
    return jsonify(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'name' not in data or 'email' not in data:
        raise BadRequest('Name and email are required')
    
    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'email': data['email']
    }
    users.append(new_user)
    
    return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = find_user(user_id)
    if not user:
        raise NotFound(f'User {user_id} not found')
    
    data = request.json
    if not data:
        raise BadRequest('No data provided')
    
    user.update({
        'name': data.get('name', user['name']),
        'email': data.get('email', user['email'])
    })
    
    return jsonify(user)

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = find_user(user_id)
    if not user:
        raise NotFound(f'User {user_id} not found')
    
    users.remove(user)
    return '', 204

# Post endpoints
@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify({
        'posts': posts,
        'total': len(posts)
    })

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = find_post(post_id)
    if not post:
        raise NotFound(f'Post {post_id} not found')
    
    return jsonify(post)

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    if not data or 'title' not in data or 'content' not in data or 'user_id' not in data:
        raise BadRequest('Title, content, and user_id are required')
    
    # Verify user exists
    if not find_user(data['user_id']):
        raise BadRequest(f'User {data["user_id"]} not found')
    
    new_post = {
        'id': len(posts) + 1,
        'title': data['title'],
        'content': data['content'],
        'user_id': data['user_id']
    }
    posts.append(new_post)
    
    return jsonify(new_post), 201

@app.route('/api/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    if not find_user(user_id):
        raise NotFound(f'User {user_id} not found')
    
    user_posts = [post for post in posts if post['user_id'] == user_id]
    return jsonify({
        'posts': user_posts,
        'total': len(user_posts),
        'user_id': user_id
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Enable CORS for cross-origin requests
    app.enable_cors()
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)
