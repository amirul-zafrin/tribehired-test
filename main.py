from fastapi import FastAPI
from collections import Counter
import uvicorn

from utils import call_api, sort_keyval, sort_list_query
import schemas

app = FastAPI()

@app.get("/posts", response_model=schemas.PostsList)
async def get_posts_ordered_by_comments():
    comments = await call_api('https://jsonplaceholder.typicode.com/comments')
    posts = await call_api('https://jsonplaceholder.typicode.com/posts')
    post_comment = Counter(x['postId'] for x in comments)
    sorted_post_comment = dict(sorted(post_comment.items(), key=sort_keyval))
    resp = sorted(posts, key=lambda x: sorted_post_comment.get(x['id']))
    respo = []
    for r in list(reversed(resp)):
        remapped = {f"post_{key}": val for key,val in r.items()}
        respo.append({**remapped, "total_number_of_comments" : sorted_post_comment.get(r['id'])})
    
    return {"posts": respo}

@app.get("/comments", response_model=schemas.CommentsList)
async def get_filtered_comments(postId: int | None = None, id: int | None = None, name: str | None = None, email: str | None = None, body: str | None = None):
    comments = await call_api('https://jsonplaceholder.typicode.com/comments')
    requests = {"postId": postId, "id": id, "name": name, "email": email, "body": body}
    for request in list(requests.keys()):
        comments = sort_list_query(comments, request, requests[request])
    resp = []
    for c in comments:
        remapped = {
            "comment_id":c["id"],
            "post_id": c["postId"],
            "user_name": c["name"],
            "user_email": c["email"],
            "post_body": c["body"]
            }
        resp.append({**remapped})
    return {"comments": resp}
