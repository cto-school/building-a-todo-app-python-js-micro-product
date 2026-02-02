# =============================================================================
# Part 5: Todo CRUD
# =============================================================================
# Now we add Create, Read, Update, Delete operations for todos.
# We will learn:
#   1. CRUD operations (Create, Read, Update, Delete)
#   2. RESTful API endpoints
#   3. Frontend JavaScript to call APIs
#
# NOTE: In this part, todos are NOT protected yet.
#       We'll add authentication in Part 6.
# =============================================================================

from flask import Flask, render_template, request, jsonify
from models import db, User, Todo, init_db
from auth import hash_password, verify_password, create_token

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
# TODO CRUD API ROUTES
# =============================================================================

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """
    READ - Get all todos for a user.

    For now, we get user_id from query parameter (not secure).
    In Part 6, we'll get it from the JWT token.
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    todos = Todo.query.filter_by(user_id=user_id).all()

    return jsonify({
        'todos': [{
            'id': t.id,
            'task_content': t.task_content,
            'is_completed': t.is_completed
        } for t in todos]
    }), 200


@app.route('/api/todos', methods=['POST'])
def create_todo():
    """
    CREATE - Add a new todo.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    task_content = data.get('task_content')
    user_id = data.get('user_id')

    if not task_content or not user_id:
        return jsonify({'error': 'task_content and user_id required'}), 400

    todo = Todo(
        task_content=task_content,
        is_completed=False,
        user_id=user_id
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
def update_todo(todo_id):
    """
    UPDATE - Modify an existing todo.
    """
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

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
def delete_todo(todo_id):
    """
    DELETE - Remove a todo.
    """
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted!'}), 200


# =============================================================================
# RUN THE SERVER
# =============================================================================
if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Part 5: Todo CRUD")
    print("  Open: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True)


# ============================================
# SELF-STUDY QUESTIONS
# ============================================
# 1. What does CRUD stand for?
# 2. What HTTP methods are used for each CRUD operation?
#    - Create = ?  Read = ?  Update = ?  Delete = ?
# 3. What is the problem with getting user_id from request.args?
# 4. Why do we use todo_id in the URL for PUT and DELETE?
# 5. What does status code 404 mean?
#
# ============================================
# ACTIVITIES - Try These!
# ============================================
# Activity 1: See the security problem
#   - Login as User A, note the user_id
#   - Open browser console and run:
#     fetch('/api/todos?user_id=1')  // Try different user_ids
#   - You can see OTHER users' todos! (This is bad!)
#   - We'll fix this in Part 6
#
# Activity 2: Add search feature
#   - Modify get_todos() to accept 'search' query parameter
#   - Filter todos where task_content contains the search term
#   - Hint: Todo.query.filter(Todo.task_content.contains(search))
#
# Activity 3: Add sorting
#   - Sort todos by created_at date
#   - Hint: Todo.query.filter_by(...).order_by(Todo.created_at.desc())
#
# Activity 4: Add pagination
#   - Only return 10 todos per page
#   - Accept 'page' parameter in URL
#   - Hint: .paginate(page=page, per_page=10)
# ============================================
