from flask import Flask, request, jsonify, render_template
from models import db, User, Todo
from auth import hash_password, verify_password, create_token, token_required, admin_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    # Create default admin user if not exists
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=hash_password('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('\n' + '='*50)
        print('DEFAULT ADMIN USER CREATED:')
        print('Email:    admin@example.com')
        print('Password: admin123')
        print('='*50 + '\n')
    else:
        print('\n' + '='*50)
        print('ADMIN LOGIN:')
        print('Email:    admin@example.com')
        print('Password: admin123')
        print('='*50 + '\n')


# ============================================
# PAGE ROUTES
# ============================================

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

@app.route('/admin')
def admin_page():
    return render_template('admin.html')


# ============================================
# AUTH API
# ============================================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400

    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hash_password(data['password'])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if not user or not verify_password(data['password'], user.password_hash):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = create_token(user.id)

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin  # Include admin status
        }
    })


# ============================================
# TODO API (Protected)
# ============================================

@app.route('/api/todos', methods=['GET'])
@token_required
def get_todos(current_user):
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return jsonify({'todos': [todo.to_dict() for todo in todos]})


@app.route('/api/todos', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()

    todo = Todo(
        task_content=data['task_content'],
        user_id=current_user.id
    )

    db.session.add(todo)
    db.session.commit()

    return jsonify(todo.to_dict()), 201


@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
@token_required
def update_todo(current_user, todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if todo.user_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403

    data = request.get_json()
    if 'task_content' in data:
        todo.task_content = data['task_content']
    if 'is_completed' in data:
        todo.is_completed = data['is_completed']

    db.session.commit()
    return jsonify(todo.to_dict())


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if todo.user_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted'})


# ============================================
# ADMIN API (Admin Only)
# ============================================

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_all_users(current_user):
    users = User.query.all()
    return jsonify({'users': [user.to_dict_with_stats() for user in users]})


@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_user, user_id):
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot delete yourself'}), 400

    user = User.query.get_or_404(user_id)

    # Delete user's todos first
    Todo.query.filter_by(user_id=user_id).delete()

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User {user.username} deleted'})


@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def get_stats(current_user):
    total_users = User.query.count()
    total_todos = Todo.query.count()
    completed_todos = Todo.query.filter_by(is_completed=True).count()

    return jsonify({
        'total_users': total_users,
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'pending_todos': total_todos - completed_todos
    })


@app.route('/api/admin/todos', methods=['GET'])
@admin_required
def get_all_todos(current_user):
    """Get all todos from all users (Admin only)"""
    todos = Todo.query.all()
    result = []
    for todo in todos:
        todo_data = todo.to_dict()
        # Add username to each todo
        todo_data['username'] = todo.user.username
        result.append(todo_data)
    return jsonify({'todos': result})


if __name__ == '__main__':
    app.run(debug=True)


# ============================================
# SELF-STUDY QUESTIONS
# ============================================
# 1. What is the difference between @token_required and @admin_required?
# 2. Why do we return 403 (Forbidden) instead of 401 (Unauthorized) for non-admins?
# 3. What happens if admin tries to delete themselves?
# 4. How does to_dict_with_stats() calculate todo statistics?
#
# ============================================
# ACTIVITIES - Try These!
# ============================================
# Activity 1: Change admin password
#   - Find where 'admin123' is set and change it to 'secret456'
#   - Delete todo.db file and restart app
#   - Try logging in with new password
#
# Activity 2: Add "Make Admin" feature
#   - Create new route: PUT /api/admin/users/<id>/make-admin
#   - This should set is_admin=True for that user
#   - Test by making a regular user an admin
#
# Activity 3: Show admin badge in navbar
#   - In dashboard.html, show "Admin" badge next to username if user.is_admin
#   - Hint: Use Bootstrap badge class
#
# Activity 4: Prevent deleting other admins
#   - In delete_user(), check if target user is also admin
#   - Return error "Cannot delete another admin"
# ============================================
