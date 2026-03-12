from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .services.ai import agent_reply
from .services.auth import authenticate, issue_session, read_session
from .services.data_store import competitors, leads, market_snapshot, procurement_scores, publish_tasks, sales_recommendation

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="CopperTrade Agent AI")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def current_user(request: Request) -> Optional[dict]:
    return read_session(request.cookies.get("session"))

def require_user(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return user

@app.get("/healthz")
def healthz(): return {"status":"ok"}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = current_user(request)
    if not user: return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("dashboard.html", {"request":request, "user":user, "market":market_snapshot(), "suppliers":procurement_scores(), "competitors":competitors(), "leads":leads(), "sales":sales_recommendation(), "tasks":publish_tasks()})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request): return templates.TemplateResponse("login.html", {"request":request, "error":None})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate(username, password)
    if not user: return templates.TemplateResponse("login.html", {"request":request, "error":"账号或密码错误"}, status_code=401)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie("session", issue_session(user), httponly=True, samesite="lax")
    return response

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302); response.delete_cookie("session"); return response

@app.get("/agents", response_class=HTMLResponse)
def agents_page(request: Request):
    user = require_user(request)
    if not isinstance(user, dict): return user
    return templates.TemplateResponse("agents.html", {"request":request, "user":user})

@app.post("/api/agent")
def api_agent(request: Request, agent_type: str = Form(...), question: str = Form(...)):
    user = require_user(request)
    if not isinstance(user, dict): return JSONResponse({"error":"unauthorized"}, status_code=401)
    return agent_reply(agent_type, question)

@app.get("/api/dashboard")
def api_dashboard(request: Request):
    user = require_user(request)
    if not isinstance(user, dict): return JSONResponse({"error":"unauthorized"}, status_code=401)
    return {"market":market_snapshot(),"suppliers":procurement_scores(),"competitors":competitors(),"leads":leads(),"sales":sales_recommendation(),"tasks":publish_tasks()}
