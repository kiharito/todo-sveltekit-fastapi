from sqlalchemy.orm import Session

import models
import schemas


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, current_task: models.Task, task: schemas.TaskUpdate):
    current_task.title = task.title
    db.add(current_task)
    db.commit()
    db.refresh(current_task)
    return current_task


def read_task(db: Session, task_id: int):
    return db.get(models.Task, task_id)


def delete_task(db: Session, current_task: models.Task):
    db.delete(current_task)
    db.commit()
