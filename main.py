from fastapi import FastAPI


app = FastAPI(description='blog api')

@app.get('/blog')
def index():
  return {
    'data': 'blog list'
  }


@app.get('/blog/unpublished')
def unpublished():
  return 'jk'

@app.get('/blog/{blog_id}')
def view_blog(blog_id: int) -> dict:
  return {
    'data': blog_id
  }

@app.get('/blog/{blog_id}/comments')
def view_blog_comments(blog_id: int) -> dict:
  return {
    'data': [1, 2]
  }



