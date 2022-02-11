
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schema, utils
from .database import engine, get_db 
from .routers import post, user, auth
from pydantic import BaseSettings





models.Base.metadata.create_all(bind=engine)

app = FastAPI()

'''
######OPTIONAL (USED FOR RAW SQL)(ALTERNATIVE IS SQLALCHEMY)
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='FastAPI', user='postgres', password='Goblinsorc963', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('success!')
        break
    except Exception as error:
        print('Fail!')
        print('Error', error)
        time.sleep(2)

'''
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router) 
 
@app.get("/")
def root():
    return{"message": "Hi"}
