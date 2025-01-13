from fastapi import FastAPI
from api import add_knowgle
from api import chat_bot
app = FastAPI()

# Đăng ký các router
app.include_router(add_knowgle.router)
app.include_router(chat_bot)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)