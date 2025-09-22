from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas, curd

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Project Tracker API")

# Projects
@app.post("/projects", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    return crud.create_project(db, project)

@app.get("/projects", response_model=List[schemas.ProjectResponse])
def list_projects(db: Session = Depends(database.get_db)):
    return crud.get_projects(db)

@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(database.get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Columns
@app.post("/columns", response_model=schemas.ColumnResponse)
def create_column(column: schemas.ColumnCreate, db: Session = Depends(database.get_db)):
    return crud.create_column(db, column)

@app.get("/projects/{project_id}/columns", response_model=List[schemas.ColumnResponse])
def list_columns(project_id: int, db: Session = Depends(database.get_db)):
    return crud.get_columns_by_project(db, project_id)

# Tasks
@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db, task)

@app.get("/columns/{column_id}/tasks", response_model=List[schemas.TaskResponse])
def list_tasks(column_id: int, db: Session = Depends(database.get_db)):
    return crud.get_tasks_by_column(db, column_id)

@app.put("/tasks/{task_id}/move", response_model=schemas.TaskResponse)
def move_task(task_id: int, new_column_id: int, new_order: int, db: Session = Depends(database.get_db)):
    task = crud.update_task_order_and_column(db, task_id, new_column_id, new_order)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
