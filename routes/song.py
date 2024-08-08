import uuid
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.params import Depends
from database import get_db
from sqlalchemy.orm import Session
from middleware.auth_middleware import auth_middleware
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

router = APIRouter()

cloudinary.config( 
    cloud_name = "dup7xlrps", 
    api_key = "829429257257276", 
    api_secret = "QeRl7JSfEbNmoqpfdSJ6W7UvvTI", 
    secure=True
)

@router.post('/upload')
def upload_song(song: UploadFile = File(...),
                thumbnail: UploadFile = File(...),
                artist: str = Form(...),
                song_name: str = Form(...),
                hex_code: str = Form(...),
                db: Session = Depends(get_db),
                auth_dict = Depends(auth_middleware),
                ):
    song_id = str(uuid.uuid4())
    song_res = cloudinary.uploader.upload(song.file, resource_type='auto', folder=f'songs/{song_id}')
    print(song_res)
    thumbnail_res = cloudinary.uploader.upload(thumbnail.file, resource_type='image', folder=f'songs/{song_id}')
    print(thumbnail_res)
    # store data into db
    return 'ok'
