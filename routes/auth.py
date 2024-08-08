
import uuid
import bcrypt
from fastapi import Depends, HTTPException, Header
from middleware.auth_middleware import auth_middleware
from models.user import User
from pydancti_schemas.user_create import UserCreate
from fastapi import APIRouter
from database import get_db
from sqlalchemy.orm import Session
from pydancti_schemas.user_login import UserLogin
import jwt

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
    
    token = jwt.encode({'id': user_db.id}, 'password_key')
    # TODO: store 'password_key' in env file for safety

    return {'token': token, 'user': user_db}

@router.get('/')
def current_user_data(db: Session = Depends(get_db), user_dict = Depends(auth_middleware)):
    user = db.query(User).filter(User.id == user_dict['uid']).first()
    if not user:
        raise HTTPException(404, 'User not found')
    return user

@router.post('/upload')
def upload_song():
    # song_id = str(uuid.uuid4())
    # song_res = cloudinary.uploader.upload(song.file, resource_type='auto', folder=f'songs/{song_id}')
    print('test Ankita')
    # store data into db
    return 'ok'