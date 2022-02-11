from .. import models, schema, oauth2
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db 


router = APIRouter(prefix = "/posts" ,tags = ['Posts'])

@router.get("/", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db),  current_user : int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * from posts """)
    #posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post) 

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #print(**post.dict())
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post )
    return new_post
    
@router.get("/{id}",response_model=schema.Post)    
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" Select * from posts where id = %s  """, (str(id),))
    #post = cursor.fetchone()
    #
    #post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return post
'''
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
'''
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    #cursor.execute("""delete from posts where id = %s returning *""", (str(id),))
    #delete_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return {'message" : "deleted'}

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    #cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()