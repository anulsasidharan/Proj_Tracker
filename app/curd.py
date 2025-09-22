from sqlalchemy.orm import Session
from . import models, schemas

# Projects
def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session):
    return db.query(models.Project).all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

# Columns
def create_column(db: Session, column: schemas.ColumnCreate):
    db_column = models.Column(**column.dict())
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column

def get_columns_by_project(db: Session, project_id: int):
    return db.query(models.Column).filter(models.Column.project_id == project_id).order_by(models.Column.order).all()

# Tasks
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_column(db: Session, column_id: int):
    return db.query(models.Task).filter(models.Task.column_id == column_id).order_by(models.Task.order).all()

def update_task_order_and_column(db: Session, task_id: int, new_column_id: int, new_order: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.column_id = new_column_id
        task.order = new_order
        db.commit()
        db.refresh(task)
    return task
