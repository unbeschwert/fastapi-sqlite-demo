from helper_classes import *

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
database = Database()

@app.get("/")
def read_root():
    return {"message" : "hello world!"}

@app.post("/user/create", response_model=Reply)
def create_user(user: User):
    '''
    Creates a user. Raises a HTTPException when 
    user already exists
    '''
    if database.user_exists(user.id.bytes_le):
        raise HTTPException(status_code=409, detail="User already exists")
    database.create_user(user.id.bytes_le, user.name, 
                    user.favorite_tv_show.value)
    return JSONResponse(status_code=200,
                content={"status" : "Success", "message" : "User created!"})

@app.patch("/user/modify/{id}", response_model=Reply)
def modify_user(id : UUID, name : Optional[str] = None, 
            favorite_tv_show : Optional[TVShow] = None):
    '''
    Modifies either the name or the favorite show
    of an existing user
    '''
    if not database.user_exists(id.bytes_le):
        raise HTTPException(status_code=404, detail="User doesn't exists")        
    database.modify_user(id.bytes_le, name, favorite_tv_show)
    return JSONResponse(status_code=200,
                content={"status" : "Success", "message" : "User data modified"})

@app.delete("/user/delete/{id}", response_model=Reply)
def delete_user(id : UUID):
    '''
    Deletes the user data for a given id
    '''
    if not database.user_exists(id.bytes_le):
        raise HTTPException(status_code=404, detail="User doesn't exists")
    database.delete_user(id.bytes_le)
    return JSONResponse(status_code=200,
                content={"status" : "Success", "message" : "User data deleted"})

@app.get("/users/find/{tv_show}", response_model=Reply)
def find_users(tv_show: TVShow):
    '''
    Returns a list of users whose favorite tv show is
    given is 'tv_show'
    '''
    users = database.find_users(tv_show.value)
    return JSONResponse(status_code=200, content=users)
