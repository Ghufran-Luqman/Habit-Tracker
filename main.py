from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
import ast

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key="AJs2?]*Zp~u,Ux>Ct{3hf5k[MyB4H#7/c`S!r:'KPeY=Gzm")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, alert: str = None):
    notthere = True
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT name FROM tasks WHERE status = 'active' ORDER BY id")
    tasks = c.fetchall()
    c.execute("SELECT state FROM tasks WHERE status = 'active' ORDER BY id")
    state = c.fetchall()
    conn.commit()
    conn.close()
    if 'remove' in request.session:
        notthere = False
        if len(request.session['remove']) == 0:
            notthere = True
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks, "states": state,  "alert": alert, "notthere": notthere})

@app.post("/submit", response_class=HTMLResponse)
async def handle_input(request: Request, inputs: str = Form(...)):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    alert = ""
    inputs = inputs.strip()
    try:
        c.execute("INSERT INTO tasks (name) VALUES (?)", (inputs,))
    except Exception as e:
        try:
            c.execute("SELECT status FROM tasks WHERE name=?", (inputs,))
            if c.fetchall()[0][0] == 'removed':
                #change the state back to active
                c.execute("UPDATE tasks SET status = 'active' WHERE name=?", (inputs,))
                #remove it from the global list
                if 'remove' in request.session:
                    request.session['remove'].remove(inputs)
            else:
                alert = "alrthere"
        except Exception as e2:
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
    request.session.clear()
    return RedirectResponse("/", status_code=303)

@app.post("/ticking", response_class=HTMLResponse)
async def ticking(request: Request, tickbox: str=Form(...)):
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
        print("errorr")
        conn.commit()
        conn.close()
    return RedirectResponse("/", status_code=303)

@app.post("/remove", response_class=HTMLResponse)
async def remove(request: Request, remove: str=Form(...)):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    remove = ast.literal_eval(remove)
    remove = remove[0]
    if 'remove' not in request.session:
        request.session['remove'] = []
    request.session['remove'].append(remove)
    if len(request.session['remove']) > 10:#size of this is limited to 10 so does not cause excessive memory usage
        del request.session['remove'][0]
    c.execute("UPDATE tasks SET status = 'removed' WHERE name=?", (remove,))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

@app.post("/undo", response_class=HTMLResponse)
async def undo(request: Request):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    mostrecent = request.session['remove'][-1]
    c.execute("UPDATE tasks SET status = 'active' WHERE name=?", (mostrecent,))
    request.session['remove'].pop()
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)