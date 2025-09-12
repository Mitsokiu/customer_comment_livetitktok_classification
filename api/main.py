from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
from fastapi import FastAPI , HTTPException
import asyncio
from modul.load_model import predict
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
app = FastAPI()

# Global client + lưu comment
client: TikTokLiveClient | None = None
comments: list[dict] = []   # chứa user, comment, prediction

def log_comment(user, comment):
    pred_id = predict(comment)
    data = {
        "user": user,
        "comment": comment,
        "prediction": pred_id
    }
    comments.append(data)   # lưu vào list
    print(data)             # log ra console

# Hàm đăng ký event cho client
def register_events(client: TikTokLiveClient):
    @client.on(CommentEvent)
    async def on_comment(event: CommentEvent):
        log_comment(event.user.nickname, event.comment)

@app.post("/submit-username")
def submit_username(username: str):
    global client, comments
    comments = []  # reset list khi đổi username
    client = TikTokLiveClient(unique_id=username)
    register_events(client)
    return {"message": f"Username {username} received"}

@app.get("/send_cmt")
async def send_cmt():
    global client
    if client is None:
        return {"error": "No username set. Call /submit-username first"}
    asyncio.create_task(client.start())  # chạy async không chặn FastAPI
    return {"message": "Started listening to comments"}

# @app.get("/get_comments")
# def get_comments():
#     return {"comments": comments}

@app.get("/get_comments")
def get_comments():
    global comments
    data = comments.copy()
    comments = []   # clear sau khi trả
    return {"comments": data}


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
