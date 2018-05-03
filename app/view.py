from app import app
from .blog import blog

app.register_blueprint(blog, url_prefix='/blog')
