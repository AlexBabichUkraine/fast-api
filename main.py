from fastapi import FastAPI, Request, status
from pydantic import BaseModel
from db import database as db
import sqlite3
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')


# connection = sqlite3.connect('my_records.sqlite3')
# cursor = connection.cursor()
# query = """
#     CREATE TABLE IF NOT EXISTS records(
#         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#         title VARCHAR(100) NOT NULL,
#         author VARCHAR(50) NOT NULL,
#         description TEXT NOT NULL,
#         creation_date VARCHAR(50) NOT NULL
#         )
# """
# cursor.execute(query)

class Record(BaseModel):
    title: str
    author: str
    description: str


class NewBlogPost(BaseModel):
    title: str
    author: str
    description: str


class FullInfoBlogPost(NewBlogPost):
    pk: int
    creation_date: str


# WEB
@app.get("/all_posts")
def read_records():
    connection = sqlite3.connect('my_records.sqlite3')
    cursor = connection.cursor()
    query = """
            SELECT id, title, author, description, creation_date FROM records
            ORDER BY id DESC
            LIMIT 5
        """
    result = cursor.execute(query).fetchall()
    return result


@app.get('/')
def main(request: Request):
    limit_temp = request.query_params.get('limit')
    if limit_temp == 'all':
        result = db.read_base()
    else:
        result = db.read_base(limit=5)
    result_json = [
        dict(
            id=data[0],
            title=data[1],
            author=data[2],
            description=data[3],
            creation_date=data[4]) for data in result
    ]
    context = {
        'title': 'First page',
        'request': request,
        'result': result_json,
    }

    return templates.TemplateResponse('index.html', context=context)


# API

@app.get('/api/get_posts')
def get_posts(limit: int = 5) -> list[FullInfoBlogPost]:
    records = db.get_limited_records(limit=limit)
    records_serialized = [
        FullInfoBlogPost(
            pk=record[0],
            title=record[1],
            author=record[2],
            description=record[3],
            creation_date=record[4],
        ) for record in records
    ]
    return records_serialized


@app.get('/api/record_search')
def record_search(query_str: str = '') -> list[FullInfoBlogPost]:
    records = db.get_record_by_search(query_str=query_str)
    records_serialized = [
        FullInfoBlogPost(
            pk=record[0],
            title=record[1],
            author=record[2],
            description=record[3],
            creation_date=record[4],
        ) for record in records
    ]
    return records_serialized


@app.post("/api/add_post", status_code=status.HTTP_201_CREATED)
def add_post(record: NewBlogPost):
    db.add_record(
        title=record.title,
        author=record.author,
        description=record.description
    )
    return record
