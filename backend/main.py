from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import subprocess
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)



@app.post("/api/download")
async def download_video(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return JSONResponse(status_code=400, content={"error": "Missing URL"})

    uid = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, f"{uid}.%(ext)s")

    try:
        subprocess.run([
            "yt-dlp", "-f", "best", "-o", output_path, url
        ], check=True)

        # Find the actual downloaded file
        files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(uid)]
        if not files:
            raise Exception("Download failed")
        return {"filename": files[0]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/downloads/{filename}")
def get_download(filename: str):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "File not found"})
    return FileResponse(path=file_path, filename=filename)

app.mount("/", StaticFiles(directory="frontend/build", html=True), name="frontend")