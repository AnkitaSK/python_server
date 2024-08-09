import uuid
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.params import Depends
from database import get_db
from sqlalchemy.orm import Session
from middleware.auth_middleware import auth_middleware
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

from models.song import Song

router = APIRouter()

cloudinary.config( 
    cloud_name = "dup7xlrps", 
    api_key = "829429257257276", 
    api_secret = "QeRl7JSfEbNmoqpfdSJ6W7UvvTI", 
    secure=True
)

@router.post('/upload',status_code=201)
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
    thumbnail_res = cloudinary.uploader.upload(thumbnail.file, resource_type='image', folder=f'songs/{song_id}')
    
    new_song = Song(
        id=song_id,
        song_name=song_name,
        artist=artist,
        hex_code= hex_code,
        song_url=song_res['url'],
        thumbnail_url=thumbnail_res['url'],
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song
