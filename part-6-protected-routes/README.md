# Part 6: Protected Routes

## What You Will Learn
- @token_required decorator
- Authorization header
- User ownership verification

## Files in This Part
```
part-6-protected-routes/
├── app.py              # Flask app with protected routes
├── models.py           # Database models
├── auth.py             # Auth with token_required decorator
├── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html      # Home page
│   ├── register.html   # Registration form
│   ├── login.html      # Login form
│   └── dashboard.html  # Protected dashboard
```

## How to Run
```bash
cd part-6-protected-routes
pip install -r requirements.txt
python app.py
```
Open: http://127.0.0.1:5000

## Key Concepts

### 1. @token_required Decorator
```python
@app.route('/api/todos')
@token_required
def get_todos(current_user):
    # current_user is automatically available!
    todos = Todo.query.filter_by(user_id=current_user.id).all()
```

### 2. Authorization Header
```javascript
fetch('/api/todos', {
    headers: {
        'Authorization': 'Bearer ' + token
    }
})
```

### 3. Ownership Check
```python
if todo.user_id != current_user.id:
    return jsonify({'error': 'Unauthorized'}), 403
```

### How the Decorator Works
```python
def token_required(f):
    def decorated(*args, **kwargs):
        # 1. Get token from header
        token = request.headers['Authorization'].split(' ')[1]

        # 2. Decode token to get user_id
        user_id = decode_token(token)

        # 3. Get user from database
        current_user = User.query.get(user_id)

        # 4. Pass user to the route function
        return f(current_user, *args, **kwargs)
    return decorated
```

## Next Part
In Part 7, we will add admin panel to manage users.
