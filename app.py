from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import sqlite3

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
async def index(request: Request):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.post("/add")
async def add_item(name: str = Form(...), description: str = Form(...)):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/")

@app.route("/edit/{item_id}", methods=["GET", "POST"])
async def edit_item(request: Request, item_id: int):
    if request.method == "POST":
        form = await request.form()
        name = form["name"]
        description = form["description"]
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE items SET name=?, description=? WHERE id=?', (name, description, item_id))
        conn.commit()
        conn.close()
        
        return RedirectResponse(url="/")
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id=?', (item_id,))
    item = cursor.fetchone()
    conn.close()
    
    return templates.TemplateResponse("edit.html", {"request": request, "item": item})

@app.get("/delete/{item_id}")
async def delete_item(item_id: int):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id=?', (item_id,))
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/")

