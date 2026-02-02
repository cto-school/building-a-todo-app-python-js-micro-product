# Part 7: Admin Panel

## What You Will Learn
- is_admin field for users
- @admin_required decorator
- Admin dashboard with statistics
- User management (delete users)

## Files in This Part
```
part-7-admin-panel/
├── app.py              # Flask app with admin routes
├── models.py           # User model with is_admin field
├── auth.py             # Auth with admin_required decorator
├── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html      # Home page
│   ├── register.html   # Registration form
│   ├── login.html      # Login form
│   ├── dashboard.html  # User dashboard
│   └── admin.html      # Admin panel
```

## How to Run
```bash
cd part-7-admin-panel
pip install -r requirements.txt
python app.py
```

## Default Admin Credentials
When you run the app, it creates a default admin:
```
Email:    admin@example.com
Password: admin123
```

Open: http://127.0.0.1:5000

## Key Concepts

### 1. Admin Field in User Model
```python
class User(db.Model):
    is_admin = db.Column(db.Boolean, default=False)
```

### 2. @admin_required Decorator
```python
@app.route('/api/admin/users')
@admin_required
def get_all_users(current_user):
    # Only users with is_admin=True can access
    # Returns 403 if not admin
```

### 3. Admin vs Token Required
```python
@token_required  # Any logged-in user
@admin_required  # Only admins (is_admin=True)
```

### Admin API Routes
| Route                      | Method | Description        |
|----------------------------|--------|--------------------|
| /api/admin/users           | GET    | Get all users      |
| /api/admin/users/:id       | DELETE | Delete a user      |
| /api/admin/stats           | GET    | Get statistics     |
| /api/admin/todos           | GET    | Get all todos      |

## Next Part
Part 8 is your homework! Add priority feature to todos.
