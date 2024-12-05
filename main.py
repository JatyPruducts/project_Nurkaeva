from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel, Field

# uvicorn main:app --reload
app = FastAPI()


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


class User(BaseModel):
    id: int
    name: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


class UserCreate(BaseModel):
    name: Annotated[
        str, Field(..., title="User name", min_length=2, max_length=20)
    ]
    age: Annotated[int, Field(...,title="User age", ge=1, le=120)]


users = [
    {"id": 1, "name": "John", "age": 30},
    {"id": 2, "name": "Jane", "age": 25},
    {"id": 3, "name": "Bob", "age": 40},
]

posts = [
    {"id": 1, "title": "News_1", "body": "Text_1", "author": users[1]},
    {"id": 2, "title": "News_2", "body": "Text_2", "author": users[0]},
    {"id": 3, "title": "News_3", "body": "Text_3", "author": users[2]},
]


@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]


@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next((user for user in users if user["id"] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")
    new_post_id = len(posts) + 1
    new_post = {"id": new_post_id, "title": post.title, "body": post.body, "author": author}
    posts.append(new_post)

    return Post(**new_post)


@app.get("/items/{id}")
async def items_id(id: Annotated[int, Path(..., title='Указываем ID поста', ge=1, lt=100)]) -> Post:  # ge=1 - минимальное значение
    for post in posts:
        if post["id"] == id:
            return Post(**post)
    raise HTTPException(status_code=404, detail="Item not found")  # вывод ошибки


@app.get("/search")
async def search(post_id: Annotated[
    Optional[int],
    Query(title='ID of post to search for', ge=1, le=50)]
) -> Dict[str, Optional[Post]]:
    # http://127.0.0.1:8000/search?post_id=1
    if post_id:
        for post in posts:
            if post["id"] == post_id:
                return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"data": None}


@app.post("/user/add")
async def add_user(user: Annotated[
    UserCreate,
    Body(..., example={
        "name": "UserName",
        "age": 1
    })
]) -> User:
    new_user_id = len(users) + 1
    new_user = {"id": new_user_id, "name": user.name, "age": user.age}
    users.append(new_user)

    return User(**new_user)