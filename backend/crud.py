from sqlalchemy.orm import Session

import models
import schemas


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
