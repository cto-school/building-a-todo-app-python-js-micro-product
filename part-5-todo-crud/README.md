# Part 5: Todo CRUD

## What You Will Learn
- CRUD operations (Create, Read, Update, Delete)
- RESTful API endpoints
- Frontend JavaScript to call APIs

## Files in This Part
```
part-5-todo-crud/
├── app.py              # Flask app with CRUD
├── models.py           # Database models
├── auth.py             # Authentication helpers
├── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html      # Home page
│   ├── register.html   # Registration form
│   ├── login.html      # Login form
│   └── dashboard.html  # Todo list with CRUD
```

## How to Run
```bash
cd part-5-todo-crud
pip install -r requirements.txt
python app.py
```
Open: http://127.0.0.1:5000

## Key Concepts

### CRUD = Create, Read, Update, Delete

| Operation | HTTP Method | URL Example       |
|-----------|-------------|-------------------|
| Create    | POST        | /api/todos        |
| Read      | GET         | /api/todos        |
| Update    | PUT         | /api/todos/1      |
| Delete    | DELETE      | /api/todos/1      |

### Code Examples
```python
# CREATE
@app.route('/api/todos', methods=['POST'])
def create_todo():
    todo = Todo(task_content=data['task_content'])
    db.session.add(todo)
    db.session.commit()

# READ
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify({'todos': [...]})

# UPDATE
@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)
    todo.is_completed = data['is_completed']
    db.session.commit()

# DELETE
@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
```

## Security Warning!
In this part, we get user_id from query parameter - anyone can see other users' todos! We will fix this in Part 6.

## Next Part
In Part 6, we will protect routes with authentication.
