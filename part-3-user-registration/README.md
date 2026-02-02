# Part 3: User Registration

## What You Will Learn
- How to create a registration form
- How to receive form data with POST request
- How to save user to database

## Files in This Part
```
part-3-user-registration/
├── app.py              # Flask app with registration
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html      # Home page
│   ├── register.html   # Registration form
│   └── users.html      # View all users
```

## How to Run
```bash
cd part-3-user-registration
pip install -r requirements.txt
python app.py
```
Open: http://127.0.0.1:5000/register

## Key Concepts

### 1. POST Request
```python
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    # data = {'username': '...', 'email': '...', 'password': '...'}
```

### 2. Validation
```python
if User.query.filter_by(email=email).first():
    return jsonify({'error': 'Email already registered'}), 400
```

### 3. JSON Response
```python
return jsonify({'message': 'Success!'}), 201  # 201 = Created
return jsonify({'error': 'Failed'}), 400      # 400 = Bad Request
```

## Security Warning!
In this part, passwords are stored as plain text. Go to `/users` page to see the problem! We will fix this in Part 4.

## Next Part
In Part 4, we will add secure login with password hashing.
