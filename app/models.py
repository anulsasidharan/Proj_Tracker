from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)

    projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=True)

    columns = relationship("BoardColumn", back_populates="project", cascade="all, delete-orphan")

class BoardColumn(Base):
    __tablename__ = "columns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    order = Column(Integer, nullable=False)  # position in board

    project = relationship("Project", back_populates="columns")
    tasks = relationship("Task", back_populates="column", cascade="all, delete-orphan", order_by="Task.order")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    column_id = Column(Integer, ForeignKey("columns.id"))
    order = Column(Integer, nullable=False)  # position in column

    column = relationship("BoardColumn", back_populates="tasks")
