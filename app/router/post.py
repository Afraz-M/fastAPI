from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from .. import oauth2
from sqlalchemy import func
from typing import Optional

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    return results


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # print(new_post.dict())
    # post_dict = new_post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)

    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s)
    #                 RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")
    return post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    # my_posts.pop(index)
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",
    #                (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")
    # conn.commit()

    if post.id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return {'message': 'post was successfully deleted'}


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s returning *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    update_post = post_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.update(post.dict(),
                      synchronize_session=False)
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # print(my_posts)
    # conn.commit()
    db.commit()
    db.refresh(update_post)
    return update_post
