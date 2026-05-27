from fastapi import FastAPI
from typing import TypedDict
import logging
from middleware.logger import RequestLoggingMiddleware


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs.txt"
)

app = FastAPI(
    title="Employee CRUD API",
    description="Simple APIwith dict storage",
    version="1.0.0"
)

app.add_middleware(RequestLoggingMiddleware)

class Employee(TypedDict):
    id:int
    name:str
    # email:str
    # department:str
    # salary:int
    # is_deleted:bool

E:dict[int,Employee]={}


@app.get("/")
def home():
    return "Welcome"


@app.get("/Employees",response_model=dict[int,Employee])
def a():
    return E

@app.post("/Employee/add",status_code=201)
def create(name:str):
    print("hii")
    if E:
        tid=max(E.keys())+1
        E[tid]={"id":tid,"name":name}
    else:
        E[0]={"id":0,"name":name}
    return "end"

@app.patch("Employee/update")
def empl_update():
    pass
#end point to fetch existing employees

# @app.get("/hello",tags=["hello world"],response_model=list[str])
# def hello():
#     l:list[str]=[]
#     for i in _posts.keys():
#         l.append(_posts[i]["title"])
#     return l

# @app.post("/posts", tags=["Posts"], status_code=201, response_model=PostPublic)
# def create_post(post: PostCreate):
#     global _next_id
#     global _posts
#     id = _next_id
#     _posts[_next_id] = {
#         "id": id,
#         "title": post.title,
#         "body": post.body
#     }
#     _next_id += 1

#     return _posts[id]