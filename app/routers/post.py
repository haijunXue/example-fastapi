from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db
from typing import Optional, List
from random import randrange
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", response_model=List[schemas.Post])
@router.get("/")
def get_posts(db: Session = Depends(get_db),current_user: int=Depends(oauth2.get_current_user) ):
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()
   # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #cursor.execute(""" SELECT * FROM posts""")
    #posts = db.query(models.Post).all()
    votes = db.query(models.Vote).all()
    try:
        
        results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
        posts_with_votes = []
        for post, vote_count in results:
            post_dict = post.__dict__
            post_dict["votes"] = vote_count
            # Remove the "_sa_instance_state" key added by SQLAlchemy
            post_dict.pop("_sa_instance_state", None)
            posts_with_votes.append(post_dict)

        return posts_with_votes
    except Exception as e:
        print(f"Error occurred: {e}")
    print(results)
    #posts = cursor.fetchall()
    #print(posts)
    return posts_with_votes

    posts_dict = [
        {"id": post.id, "created_at": post.created_at, "owner_id":post.owner_id,"owner":post.owner}
        for post in posts
    ]

    print(current_user.id)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    
    print(post.dict())
    
    # new_post = models.Post(
    #     title = post.title, content = post.content, published = post.published
    # )
    print(current_user.id)
    print("aaaa")
   # new_post_data = post.dict()
    #new_post_data["owner_id"] = current_user.id
    #new_post = models.Post(**new_post_data)
    new_post = models.Post(**post.dict(),owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    
    # conn.commit()
    
    # # post_dict = post.dict()
    # # post_dict['id'] = randrange(0,1000000)
    # # my_posts.routerend(post_dict)
    # return {"data": new_post}
    #print(post)
    #print(post.dict())
    #return {"data": post}
#def create_posts(payload: dict = Body(...)):
    #print(payload)
    #return {"new_post": f"title: {payload['title']} content: {payload['content']}"}
    
# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

    
#@router.get("/{id}",response_model=schemas.Post)
@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    #results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == id) \
        .first()

    if result is None:
        # Post not found
        return {"message": "Post not found"}

    post, vote_count = result

    # Create a PostoutM instance to store the result
        # Create a dictionary to store the result
    post_with_vote = {
        "post": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            # Include other attributes from the Post object if needed
        },
        "votes": vote_count
    }

    return post_with_vote
    #print(type(id))
    print(post)
    #post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id: {id} was not found"}
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    return results
    #return {"post_detail": f"Here is post {id}"}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    #index = find_index_post(id)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exit")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        
    
    
    #my_posts.pop(index)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f"post with id: {id} does not exit")
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.filter()
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exit")
    
    #post_query.update({'title': 'hey this is my updated title', 'content': 'this is my updated content'}, synchronize_session=False)
    post = post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
