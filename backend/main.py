from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .auth import get_current_user
from .sqlite_utils import init_sqlite_db, create_operation, stop_operation
from pydantic import BaseModel

app = FastAPI(title="Výrobné operácie")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_sqlite_db()

class OperationStart(BaseModel):
    user_id: int
    order_number: str
    operation_code: str

class OperationStop(BaseModel):
    operation_id: int

@app.post("/start")
def start(data: OperationStart, user=Depends(get_current_user)):
    op_id = create_operation(data.user_id, data.order_number, data.operation_code)
    return {"status": "started", "operation_id": op_id}

@app.post("/stop")
def stop(data: OperationStop, user=Depends(get_current_user)):
    success = stop_operation(data.operation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Operácia nenájdená alebo už bola ukončená")
    return {"status": "stopped"}

@app.get("/admin", response_class=FileResponse)
def admin_page():
    return FileResponse("static/admin.html", media_type="text/html")