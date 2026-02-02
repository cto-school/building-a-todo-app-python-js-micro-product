# Part 4: User Login

## What You Will Learn
- Password hashing (never store plain passwords!)
- JWT tokens for authentication
- Login/Logout flow

## Files in This Part
```
part-4-user-login/
├── app.py              # Flask app with login
├── models.py           # Database models
├── auth.py             # Authentication helpers
├── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html      # Home page
│   ├── register.html   # Registration form
│   ├── login.html      # Login form
│   └── dashboard.html  # User dashboard
```

## How to Run
```bash
cd part-4-user-login
pip install -r requirements.txt
python app.py
```
Open: http://127.0.0.1:5000

## Key Concepts

### 1. Password Hashing
```python
from werkzeug.security import generate_password_hash, check_password_hash

# When registering
password_hash = generate_password_hash('secret123')

# When logging in
is_valid = check_password_hash(password_hash, 'secret123')
```

### 2. JWT Token
```python
import jwt

# Create token after login
token = jwt.encode({
    'user_id': user.id,
    'exp': datetime.utcnow() + timedelta(hours=24)
}, SECRET_KEY, algorithm='HS256')

# Decode token to verify
payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
user_id = payload['user_id']
```

### 3. localStorage (JavaScript)
```javascript
// Save after login
localStorage.setItem('token', data.token);

// Get when needed
const token = localStorage.getItem('token');

// Clear on logout
localStorage.clear();
```

## Next Part
In Part 5, we will add todo CRUD operations.
