"""
Basic Example - Getting Started with GoFlask
"""

from goflask import GoFlask, jsonify

# Create application instance
app = GoFlask(__name__)

# Basic route
@app.route('/')
def hello():
    return 'Hello, GoFlask!'

# JSON API endpoint
@app.route('/api/status')
def status():
    return jsonify({
        'status': 'ok',
        'message': 'GoFlask is running!',
        'version': '1.0.0'
    })

# Route with parameters
@app.route('/users/<username>')
def show_user(username):
    return jsonify({
        'username': username,
        'message': f'Hello, {username}!'
    })

# Route with multiple HTTP methods
@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    from goflask.context import request
    
    if request.method == 'POST':
        return jsonify({
            'message': 'Data received',
            'method': 'POST'
        })
    else:
        return jsonify({
            'message': 'Data endpoint',
            'method': 'GET'
        })

if __name__ == '__main__':
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)
