from enum import Enum
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
import sqlite3

class TVShow(Enum):
    '''
    Enum class containing different shows. Used to constrain
    the input values of favorite tv show.
    '''
    breaking_bad = "breaking_bad"
    the_wire = "the_wire"

class Reply(BaseModel):
    '''
    Used as a response model for a successful HTTP request
    '''
    status : str
    message : str

class User(BaseModel):
    '''
    User datatype used to constrain the user create requests. 
    '''
    id : UUID
    name : str
    favorite_tv_show : TVShow

class Database():
    def __init__(self):
        self.connect_obj = sqlite3.connect(":memory:", check_same_thread=False)
        self.cursor_obj = self.connect_obj.cursor()
        self.cursor_obj.execute(f"CREATE TABLE IF NOT EXISTS Users (id BLOB PRIMARY KEY,\
                            name TEXT, favorite_tv_show TEXT)")
        self.connect_obj.commit()

    def user_exists(self, id : bytes) -> bool:
        '''
        Checks whether a user already exists in the 'Users' table. 
        If yes, it returns True. 
        '''
        count = 0
        sql_query = f"SELECT * FROM Users WHERE id=:id"
        for _ in self.cursor_obj.execute(sql_query, {"id" : id}):
            count += 1
        return True if count > 0 else False
    
    def create_user(self, id : bytes, name : str, 
                favorite_tv_show : str):
        '''
        Creates a user entry in 'User' table. 
        '''
        sql_query = f"INSERT INTO Users VALUES (?, ?, ?)"
        self.cursor_obj.execute(sql_query, (id, name, favorite_tv_show))
        self.connect_obj.commit()
    
    def delete_user(self, id : bytes):
        '''
        Deletes a user entry from 'Users' table
        '''
        sql_query = f"DELETE FROM Users WHERE id=:id"
        self.cursor_obj.execute(sql_query, {"id" : id})
        self.connect_obj.commit()
    
    def modify_user(self, id : bytes, name : Optional[str], 
                favorite_tv_show : Optional[TVShow]):
        '''
        Modfies a user entry in 'Users' table. 
        '''
        if name and favorite_tv_show:
            sql_query = f"UPDATE Users SET name=:name \
                favorite_tv_show=:favorite_tv_show WHERE id=:id"
            self.cursor_obj.execute(sql_query, 
                {"name" : name, "favorite_tv_show" : favorite_tv_show.value, "id" : id})
            self.connect_obj.commit()
        elif name and not favorite_tv_show:
            sql_query = f"UPDATE Users SET name=:name WHERE id=:id"
            self.cursor_obj.execute(sql_query, {"name" : name, "id" : id})
            self.connect_obj.commit()
        elif favorite_tv_show and not name:
            sql_query = f"UPDATE Users SET favorite_tv_show=:favorite_tv_show WHERE id=:id"
            self.cursor_obj.execute(sql_query, {"favorite_tv_show" : favorite_tv_show.value, "id" : id})
            self.connect_obj.commit()
        else:
            pass
    
    def find_users(self, favorite_tv_show : str) -> dict:
        '''
        Finds users with same favorite tv show. 
        '''
        users = {"users" : []}
        sql_query = f"SELECT * FROM Users WHERE favorite_tv_show=:favorite_tv_show"
        for user in self.cursor_obj.execute(sql_query, {"favorite_tv_show" : favorite_tv_show}):
            users["users"].append({"id" : str(UUID(bytes_le=user[0])), "name" : user[1]})
        return users
    
    def __del__(self):
        self.connect_obj.close()
