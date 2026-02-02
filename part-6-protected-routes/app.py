# =============================================================================
# Part 6: Protected Routes
# =============================================================================
# Now we protect todo routes with authentication.
# We will learn:
#   1. @token_required decorator
#   2. Authorization header
#   3. User ownership verification
# =============================================================================

from flask import Flask, render_template, request, jsonify
from models import db, User, Todo, init_db
from auth import hash_password, verify_password, create_token, token_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


# =============================================================================
# PAGE ROUTES
# =============================================================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


# =============================================================================
# AUTH API ROUTES
# =============================================================================

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password)
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful!'}), 201


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_token(user.id, user.is_admin)

    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin
        }
    }), 200


# =============================================================================
# PROTECTED TODO API ROUTES
# =============================================================================
# All routes below use @token_required decorator.
# This means:
#   1. Request must have "Authorization: Bearer <token>" header
#   2. Token must be valid and not expired
#   3. current_user is automatically passed to the function

@app.route('/api/todos', methods=['GET'])
@token_required
def get_todos(current_user):
    """Get all todos for the logged-in user."""
    todos = Todo.query.filter_by(user_id=current_user.id).all()

    return jsonify({
        'todos': [{
            'id': t.id,
            'task_content': t.task_content,
            'is_completed': t.is_completed
        } for t in todos]
    }), 200


@app.route('/api/todos', methods=['POST'])
@token_required
def create_todo(current_user):
    """Create a new todo for the logged-in user."""
    data = request.get_json()
    if not data or not data.get('task_content'):
        return jsonify({'error': 'task_content required'}), 400

    todo = Todo(
        task_content=data['task_content'],
        is_completed=False,
        user_id=current_user.id  # Automatically set from token!
    )
    db.session.add(todo)
    db.session.commit()

    return jsonify({
        'message': 'Todo created!',
        'todo': {
            'id': todo.id,
            'task_content': todo.task_content,
            'is_completed': todo.is_completed
        }
    }), 201


@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
@token_required
def update_todo(current_user, todo_id):
    """Update a todo (only if user owns it)."""
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Check ownership!
    if todo.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    if 'task_content' in data:
        todo.task_content = data['task_content']
    if 'is_completed' in data:
        todo.is_completed = data['is_completed']

    db.session.commit()

    return jsonify({
        'message': 'Todo updated!',
        'todo': {
            'id': todo.id,
            'task_content': todo.task_content,
            'is_completed': todo.is_completed
        }
    }), 200


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    """Delete a todo (only if user owns it)."""
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    # Check ownership!
    if todo.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted!'}), 200


# =============================================================================
# RUN THE SERVER
# =============================================================================
if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Part 6: Protected Routes")
    print("  Open: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True)


# ============================================
# SELF-STUDY QUESTIONS
# ============================================
# 1. What is a decorator in Python? What does @token_required do?
# 2. How does the Authorization header work?
# 3. What is the difference between 401 Unauthorized and 403 Forbidden?
# 4. Why do we check todo.user_id != current_user.id?
# 5. What would happen if we removed @token_required from a route?
#
# ============================================
# ACTIVITIES - Try These!
# ============================================
# Activity 1: Test without token
#   - Open browser console (F12)
#   - Try: fetch('/api/todos')
#   - You should get 401 error!
#
# Activity 2: Test with token
#   - Get token from localStorage: let token = localStorage.getItem('token')
#   - Try: fetch('/api/todos', {headers: {'Authorization': 'Bearer ' + token}})
#   - Now it works!
#
# Activity 3: Try to access other user's todo
#   - Create todo as User A (note the todo id)
#   - Login as User B
#   - Try to delete User A's todo - you should get 403 Forbidden!
#
# Activity 4: Create your own decorator
#   - Create @login_required that only checks if user is logged in
#   - Create @verified_required that checks if user email is verified
#   - Hint: Add 'is_verified' field to User model first
# ============================================
