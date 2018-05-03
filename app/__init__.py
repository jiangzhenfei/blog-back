from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#数据库的默认设置 1.包括数据库额地址 2、数据库的其他信息，没看懂需要再去认识一下
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://admin:xuyuan2017@47.93.103.19/fei'#数据库连接地址
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True
db = SQLAlchemy(app)

from app import view,model