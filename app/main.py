from typing import List
from fastapi import FastAPI, Response, status, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel,EmailStr
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas,oauth
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, get_db
from .utils import hash_password,verify_password



import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()





while True:
    try:
        conn = psycopg2.connect(host="localhost", database='postgres', user="postgres", password="123456",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to DataBase")
        break
    except Exception as error:
        print("Connection to DataBase Failed")
        print("Error:", error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Hello World"}




@app.post("/createuser",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(createuser: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == createuser.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    

    hashpw= hash_password(createuser.password)
    
    new_user = models.User(email=createuser.email, password=hashpw)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@app.get("/getuser/{id}",response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user


@app.post("/login")
def login(user_credentials:schemas.userLogin,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not verify_password(user_credentials.password,user.password) :  #compare the given password and the password saved in the db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    

    access_token= oauth.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}


        
    
  




@app.get('/posts',response_model=list[schemas.postResponse])
def get_posts(db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    posts=db.query(models.Post).all()
    try:
        posts = db.query(models.Post).all()
        print(f"Fetched posts: {posts}")
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching posts")
    return {posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post=models.Post(**post.dict())    #**post.dict() will do the post.title thing for us, we just have to unpack the dictionary
    #new_post= models.Post(title=post.title,content= post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return {"post_detail": post}
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post=db.query(models.Post).filter(models.Post.id==id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="POST NOT FOUND")
    
    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",status_code=status.HTTP_200_OK)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):
    post_query= db.query(models.Post).filter(models.Post.id==id)  #grabbing the specific post by id
    existing_post=post_query.first() 
    if existing_post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="POST NOT FOUND")
    
  

    post_query.update({
        **post.dict()
    },
    
    synchronize_session=False)

    print("bruhh")
    db.commit()



    return {"detail":"Post Updated Successfully","data":post_query.first()}
    


