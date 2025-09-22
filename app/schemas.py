from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int

class TaskCreate(TaskBase):
    column_id: int

class TaskResponse(TaskBase):
    id: int
    column_id: int
    class Config:
        orm_mode = True

class ColumnBase(BaseModel):
    name: str
    order: int

class ColumnCreate(ColumnBase):
    project_id: int

class ColumnResponse(ColumnBase):
    id: int
    project_id: int
    tasks: List[TaskResponse] = []
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    columns: List[ColumnResponse] = []
    class Config:
        orm_mode = True
