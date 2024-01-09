from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud
from . import schemas
from .database import SessionLocal

app = FastAPI()

origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/tasks/", response_model=list[schemas.Task])
async def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return tasks


@app.post("/tasks/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


@app.get("/tasks/{task_id}/", response_model=schemas.Task)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.read_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}/", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    current_task = crud.read_task(db=db, task_id=task_id)
    if current_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, current_task=current_task, task=task)


@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    current_task = crud.read_task(db=db, task_id=task_id)
    if current_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db=db, current_task=current_task)
    return {"message": "Task deleted"}
