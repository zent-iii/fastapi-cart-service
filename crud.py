import models
from sqlalchemy.orm import Session

# Korábban: load_json() és keresés listában
# SQLAlchemy-vel:
def get_user(db: Session, user_id: int):
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()