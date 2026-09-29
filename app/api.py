from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Add workspace directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.medicine_catalog import CATALOG
from app.lasa_engine import check_pick

app = FastAPI(title="LASA Dispensing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for packaging images
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

class PickRequest(BaseModel):
    intended_sku: str
    picked_sku: str
    barcode_scan_ok: Optional[bool] = None

@app.get("/", response_class=HTMLResponse)
async def read_index():
    mvp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mvp.html")
    with open(mvp_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/catalog")
async def get_catalog():
    return CATALOG

@app.post("/check_pick")
async def api_check_pick(req: PickRequest):
    result = check_pick(req.intended_sku, req.picked_sku, CATALOG, req.barcode_scan_ok)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
