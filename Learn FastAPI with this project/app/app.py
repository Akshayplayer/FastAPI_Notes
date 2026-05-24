from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.db import Post, get_async_session, create_db_and_tables
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield



app=FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file: UploadFile=File(...), # it will gone to accept a file object
    caption: str=Form(...),
    session: AsyncSession=Depends(get_async_session)
):
    temp_file_path=None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splittext(file.filename)[1]) as temp_file:
            temp_file_path=temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result= imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            filename=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )

        if upload_result.response.http_status_code==200:

            post=Post(
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )
            session.add(post) # it is like stagging post
            await session.commit() # it is like saving post.
            await session.refresh(post) # it will look  into the database and populate entries that were automatically created to the database.
            return post
    
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()

@app.get("/feed")
async def get_feed(
    session: AsyncSession=Depends(get_async_session) # because we needed database to access our data
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts=[row[0] for row in result.all()]

    posts_data=[]
    for post in posts:
        posts_data.append(
            {
                "id":str(post.id),
                "caption":post.caption,
                "url":post.url,
                "file_type":post.file_type,
                "file_name":post.file_name,
                "created_at":post.created_at.isoformat()

            }
        )

    return {"posts":posts_data}