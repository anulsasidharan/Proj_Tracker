from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas, curd, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Project Tracker API with Auth")

# Register
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Token (Login)
@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
@app.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


# Projects (protected - user only sees their own)
@app.post("/projects", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    db_project = models.Project(**project.dict(), owner_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects", response_model=List[schemas.ProjectResponse])
def list_projects(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return db.query(models.Project).filter(models.Project.owner_id == current_user.id).all()


@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == current_user.id).first()
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
