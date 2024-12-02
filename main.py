from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
import sqlite3
import ast

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, alert: str = None):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT name FROM tasks ORDER BY id")
    tasks = c.fetchall()
    c.execute("SELECT state FROM tasks ORDER BY id")
    state = c.fetchall()
    conn.commit()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks, "states": state,  "alert": alert})

@app.post("/submit", response_class=HTMLResponse)
async def handle_input(request: Request, inputs: str = Form(...)):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    alert = ""
    try:
        c.execute("INSERT INTO tasks (name) VALUES (?)", (inputs,))
    except:
        alert = "alrthere"
    conn.commit()
    conn.close()
    return RedirectResponse(url=f"/?alert={alert}", status_code=303)

@app.post("/reset", response_class=HTMLResponse)
async def reset_inputs(request: Request):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks")#deletes everything i think
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

@app.post("/ticking", response_class=HTMLResponse)
async def ticking(tickbox: str=Form(...)):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    tickbox = ast.literal_eval(tickbox)
    tickbox = tickbox[0]
    c.execute("SELECT state FROM tasks WHERE name=?", (tickbox,))
    state = c.fetchall()
    state = state[0][0]
    if state == 0:
        c.execute("UPDATE tasks SET state=? WHERE name=?", (1, tickbox))
        conn.commit()
        conn.close()
    elif state == 1:
        c.execute("UPDATE tasks SET state=? WHERE name=?", (0, tickbox))
        conn.commit()
        conn.close()
    else:
        print("idk whats going on breh this program twaeaking fr")
        conn.commit()
        conn.close()
    return RedirectResponse("/", status_code=303)