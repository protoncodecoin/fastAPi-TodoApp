from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import SessionLocal

from ..models import Users
from .auth import get_current_user
from passlib.context import CryptContext


class ChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)


class PhoneNumber(BaseModel):
    phone_number: str = Field(min_length=10)


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


@router.get("/all")
async def all_users(db: db_dependency):
    return db.query(Users).all()


@router.get("/user")
async def currently_logged_in_user(user: user_dependency, db: db_dependency):
    print(user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )

    model = db.query(Users).filter(Users.id == user.get("id")).first()

    return model


@router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(
    user: user_dependency, db: db_dependency, user_password: ChangePassword
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )

    user__obj = db.query(Users).filter(Users.id == user.get("id")).first()

    if user__obj:
        # verify old password
        if not bcrypt_context.verify(
            user_password.old_password, user__obj.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Authentication failed"
            )
        user__obj.hashed_password = bcrypt_context.hash(user_password.new_password)

        db.add(user__obj)
        db.commit()


@router.put("/change_phone_number", status_code=status.HTTP_200_OK)
async def change_phone_number(
    user: user_dependency, db: db_dependency, phone: PhoneNumber
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    user_obj = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    user_obj.phone_number = phone.phone_number

    db.add(user_obj)
    db.commit()
