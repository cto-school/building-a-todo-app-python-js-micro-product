# =============================================================================
# Part 4: User Login
# =============================================================================
# Now we add secure login with password hashing and JWT tokens.
# We will learn:
#   1. Password hashing (never store plain passwords!)
#   2. JWT tokens for authentication
#   3. Login/Logout flow
# =============================================================================

from flask import Flask, render_template, request, jsonify
from models import db, User, init_db
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
# API ROUTES
# =============================================================================

@app.route('/api/register', methods=['POST'])
def api_register():
    """Register new user with hashed password."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    # Hash the password before storing!
    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password)  # Now it's secure!
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful!'}), 201


@app.route('/api/login', methods=['POST'])
def api_login():
    """Login user and return JWT token."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Verify password
    if not user or not verify_password(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Create JWT token
    token = create_token(user.id, user.is_admin)

    return jsonify({
        'message': 'Login successful!',
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin
        }
    }), 200


# =============================================================================
# RUN THE SERVER
# =============================================================================
if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Part 4: User Login")
    print("  Open: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True)


# ============================================
# SELF-STUDY QUESTIONS
# ============================================
# 1. What is password hashing? Why can't we reverse a hash?
# 2. What is JWT? What information does it store?
# 3. Why do we store token in localStorage?
# 4. What happens when token expires?
# 5. What is the difference between 401 and 403 status codes?
#
# ============================================
# ACTIVITIES - Try These!
# ============================================
# Activity 1: See the hashed password
#   - Register a new user
#   - Open instance/todo.db with DB Browser
#   - Look at password_hash column - it's not readable!
#
# Activity 2: Decode a JWT token
#   - After login, open browser console (F12)
#   - Type: localStorage.getItem('token')
#   - Go to https://jwt.io and paste the token
#   - See what information is inside (but NOT the password!)
#
# Activity 3: Change token expiry time
#   - In auth.py, find timedelta(hours=24)
#   - Change to timedelta(minutes=5)
#   - Login and wait 5 minutes - you'll be logged out!
#
# Activity 4: Add "Remember Me" feature
#   - If user checks "Remember Me", token expires in 7 days
#   - If not checked, token expires in 1 hour
#   - Hint: Pass remember_me to create_token() function
# ============================================
