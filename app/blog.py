from flask import Flask,url_for, request, redirect, render_template,Blueprint,jsonify
import json
from app import db
from .model import Blog,User
#引入时间
from datetime import datetime


blog = Blueprint('blog',__name__)

#返回的数据格式，根据不同情况生成不同额返回值
def util_res(code=200,message='',success=True,response=None):
    return {
        'code':     code,
        'message':  message,
        'success':  success,
        'response': response
    }

#博客列表的接口
@blog.route('/list',methods=['GET'])
def list():
    res_blog = []
    blogs = Blog.query.all()
    #将数据库的数据处理发送给前端
    for item in blogs:
        if item == None:break
        item_log = {
            'title':    item.title,
            'content':  item.content,
            'summary':  item.summary,
            'id':       item.id
        }
        res_blog.append(item_log)
    resp = util_res(response = res_blog)
    return jsonify(resp)


#增加博客的接口
@blog.route('/add',methods = ['POST'])
def add():
    data = request.data.decode('utf-8')
    #json.loads将字符转成相应的对象
    j_data =  json.loads(data)
    #判断对象是否存在某些属性
    print('ddddd',j_data.get('title'))
    if not j_data.get('title'):
        resp = util_res(code = 400,message='title 是必须的',success=False)
        return jsonify(resp)
    if not j_data.get('content'):
        resp = util_res(code = 400,message='content 是必须的',success=False)
        return jsonify(resp)
    if not j_data.get('summary'):
        resp = util_res(code = 400,message='summary 是必须的',success=False)
        return jsonify(resp)
    blog_item = Blog(title = j_data['title'], content = j_data['content'],summary = j_data['summary'])
    db.session.add(blog_item)
    db.session.commit()
    resp = util_res()
    return jsonify(resp) 

#这是博客详情接口
@blog.route('/detail/<id>',methods=['GET'])
def detail(id):
    #筛选出来符合条件的第一条数据
    thisBlog = Blog.query.filter_by(id = id).first()
    if thisBlog is None:
        resp = util_res(code=400,message='改博客数据不存在',success=False)
        return jsonify(resp)
    #整理成前端需要的数据格式
    res_detail = {
        'title':thisBlog.title,
        'content':thisBlog.content,
        'summary':thisBlog.summary,
        'id':thisBlog.id
    }
    resp = util_res(response = res_detail)
    return jsonify(resp)

#用户登录界面的接口
@blog.route('/login',methods = ['POST'])
def login():
    data = request.data.decode('ascii')
    #json.loads将字符转成相应的对象
    j_data =  json.loads(data)
    #判断对象是否存在某些属性
    if not j_data.get('name'):
        resp = util_res(code = 400,message = 'name 是必须的',success = False)
        return jsonify(resp)
    if not j_data.get('password'):
        resp = util_res(code = 400,message='password 是必须的',success = False)
        return jsonify(resp)
    #在数据库获取相应的用户信息
    #用来做密码匹配的判断
    user = User.query.filter_by(name = j_data['name']).first()
    #用户不存在的判断
    #用户存在但是密码不对的判断
    #都是正确的判断
    if user is None:
        resp = util_res(code = 400,message = '该用户不存在',success = False)
        return jsonify(resp)
    if j_data['password'] == user.password:
        #每次登入更新数据库的时间戳
        user.time = datetime.now().timestamp()
        db.session.add(user)
        db.session.commit()
        resp = util_res(message = '登入成功',response = user.name)
        return jsonify(resp)
    else:
        resp = util_res(code = 400,message = '密码错误',success = False)
        return jsonify(resp)

    
    