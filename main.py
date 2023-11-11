from fastapi import FastAPI, Request, status, Form
from pydantic import BaseModel
from storage import database as db
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')


class NewBlogPost(BaseModel):
    title: str
    author: str
    description: str
    article_image: str


class FullInfoBlogPost(NewBlogPost):
    pk: int
    creation_date: str


def _serialize_posts(records: list[tuple]) -> list[FullInfoBlogPost]:
    records_serialized = [
        FullInfoBlogPost(
            pk=record[0],
            title=record[1],
            author=record[2],
            description=record[3],
            article_image=record[4],
            creation_date=record[5],
        ) for record in records
    ]
    return records_serialized


# WEB

@app.get('/', tags=['WEB'])
def main(request: Request):
    result = db.get_posts()
    posts_serialized = _serialize_posts(result)
    context = {
        'title': f'Last 5 published posts',
        'request': request,
        'posts': posts_serialized,
    }
    return templates.TemplateResponse('all_posts.html', context=context)


@app.get("/all_posts", tags=['WEB'])
@app.post("/search", tags=['WEB'])
@app.get("/search", tags=['WEB'])
def all_posts(request: Request, search_post: str = Form(None)):
    if search_post:
        result = db.get_posts_by_search(search_field=search_post)
    else:
        result = db.get_posts_by_search()
    posts_serialized = _serialize_posts(result)
    context = {
        'title': f'Founded {len(result)} posts for search: {search_post}' if search_post else 'All posts',
        'request': request,
        'posts': posts_serialized,
    }
    return templates.TemplateResponse('all_posts.html', context=context)


@app.get("/add_post", tags=['WEB'])
def add_post(request: Request):
    context = {
        'title': 'Add post',
        'request': request,
    }
    return templates.TemplateResponse('add_post.html', context=context)


@app.post("/add_post", tags=['WEB'])
def add_post_final(
        request: Request,
        title: str = Form(),
        author: str = Form(),
        description: str = Form(),
        article_image: str = Form()):
    db.add_post(
        title=title,
        author=author,
        description=description,
        article_image=article_image
    )
    result = db.get_posts(limit=5)
    posts_serialized = _serialize_posts(result)
    context = {
        'title': 'Add post',
        'request': request,
        'posts': posts_serialized
    }
    return templates.TemplateResponse('all_posts.html', context=context)


@app.get("/author/{author}")
async def read_item(author: str, request: Request):
    result = db.get_posts_by_author(author=author)
    print(author)
    posts_serialized = _serialize_posts(result)
    context = {
        'title': f'Founded {len(result)} posts by: {author}',
        'request': request,
        'posts': posts_serialized
    }
    return templates.TemplateResponse('all_posts.html', context=context)

# API


@app.get('/api/get_posts', tags=['API'])
@app.post('/api/get_posts', tags=['API'])
def get_posts(limit: int = 5) -> list[FullInfoBlogPost]:
    records = db.get_posts(limit=limit)
    return _serialize_posts(records)


@app.get('/api/post_search', tags=['API'])
def post_search(query_str: str = '') -> list[FullInfoBlogPost]:
    records = db.get_posts_by_search(search_field=query_str)
    return _serialize_posts(records)


@app.post("/api/add_post", status_code=status.HTTP_201_CREATED, tags=['API'])
def add_post(record: NewBlogPost):
    db.add_post(
        title=record.title,
        author=record.author,
        description=record.description,
        article_image=record.article_image
    )
    return record
