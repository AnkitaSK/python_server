
import uuid
import bcrypt
from fastapi import Depends, HTTPException
from models.user import User
from pydancti_schemas.user_create import UserCreate
from fastapi import APIRouter
from database import get_db
from sqlalchemy.orm import Session
from pydancti_schemas.user_login import UserLogin

router = APIRouter()

@router.post('/signup', status_code=201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    #test if the user exist - in db postgree
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(400, 'user exists')
    
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_db = User(id = str(uuid.uuid4), name = user.name, email = user.email, password = hashed_password)
    # add the user to the db
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@router.post('/login')
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    #check if the user exists
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(400, 'User doesnt exist')
    #check if password match
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)
    if not is_match:
        raise HTTPException(400, 'Wrong password')

    return user_db