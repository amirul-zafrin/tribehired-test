from pydantic import BaseModel

class PostBase(BaseModel):
    post_id: int
    post_title: str
    post_body: str

class Post(PostBase):
    total_number_of_comments: int

class PostsList(BaseModel):
    posts: list[Post]

class CommentBase(BaseModel):
    comment_id: str
    post_id: int
    user_name: str
    user_email: str
    post_body: str

class CommentsList(BaseModel):
    comments: list[CommentBase]

