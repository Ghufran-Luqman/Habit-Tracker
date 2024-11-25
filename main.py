from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

tasks = []
states = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks, "states": states})

@app.post("/submit", response_class=HTMLResponse)
async def handle_input(request: Request, inputs: str = Form(...)):
    tasks.append(inputs)
    states.append(0)
    return RedirectResponse("/", status_code=303)

@app.post("/reset", response_class=HTMLResponse)
async def reset_inputs(request: Request):
    tasks.clear()
    states.clear()
    return RedirectResponse("/", status_code=303)

@app.post("/ticking", response_class=HTMLResponse)
async def ticking(tickbox: str=Form(...)):
    position = tasks.index(tickbox)
    if states[position] == 0:#unticked
        states[position] = 1#tick
    elif states[position] == 1:#ticked
        states[position] = 0#untick
    else:
        print(f"idk waht happened bro this rpogram tweaking")
        raise UnicodeError
    return RedirectResponse("/", status_code=303)