# Part 8: Homework - Add Priority Feature

## Your Task
Add a **priority** feature (low, medium, high) to todos.

---

## 7 Simple Steps

Follow the steps in order. Each step is marked in the code with `STEP 1`, `STEP 2`, etc.

| Step | File | What to Do |
|------|------|------------|
| 1 | models.py | Uncomment `priority = db.Column(...)` |
| 2 | models.py | Uncomment `'priority': self.priority` |
| 3 | app.py | Uncomment `priority=data.get(...)` |
| 4 | dashboard.html | Uncomment the `<select>` dropdown |
| 5 | dashboard.html | Change the API call to include priority |
| 6 | dashboard.html | Uncomment `getPriorityBadge()` function |
| 7 | dashboard.html | Add `${getPriorityBadge(todo.priority)}` |

---

## How to Complete

### Step 1: models.py (line 38)
Remove the `#` to uncomment:
```python
priority = db.Column(db.String(10), default='medium')
```

### Step 2: models.py (line 51)
Remove the `#` to uncomment:
```python
'priority': self.priority
```

### Step 3: app.py (line 106)
Remove the `#` to uncomment:
```python
priority=data.get('priority', 'medium')
```

### Step 4: dashboard.html (line 40-46)
Remove `<!--` and `-->` to uncomment the select dropdown.

### Step 5: dashboard.html (line 115)
Change from:
```javascript
await api('/api/todos', 'POST', { task_content: taskContent });
```
To:
```javascript
await api('/api/todos', 'POST', { task_content: taskContent, priority: document.getElementById('priority-input').value });
```

### Step 6: dashboard.html (line 123-129)
Remove `/*` and `*/` to uncomment the function.

### Step 7: dashboard.html (line 150)
Add this line after the checkbox:
```javascript
${getPriorityBadge(todo.priority)}
```

---

## How to Test

1. **Delete old database**: Delete `instance/todo.db` file
2. **Run the app**: `python app.py`
3. **Register** a new user
4. **Add todos** with different priorities
5. **Check** if colored badges appear (High=Red, Medium=Yellow, Low=Green)

---

## Expected Result

When complete, you should see:
- A dropdown to select priority (Low/Medium/High)
- Colored badges on each todo showing its priority

---

## Check Your Answer

After completing, compare your code with the `solution/` folder.

---

## Stuck?

- Make sure you deleted `instance/todo.db` after Step 1-2
- Check browser console (F12) for errors
- Compare with `solution/` folder
