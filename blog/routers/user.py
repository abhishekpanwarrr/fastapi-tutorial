from fastapi import APIRouter, HTTPException, status,Depends
from .. import schemas, models, database, hashing
from sqlalchemy.orm import Session


router = APIRouter(tags=["Users"], prefix="/user")


@router.post("/", response_model=schemas.ShowUser)
async def crate_user(request: schemas.User, db: Session = Depends(database.get_db)):

    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=schemas.ShowUser)
async def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found!")
    return user

