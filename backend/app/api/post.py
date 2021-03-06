#!/usr/bin/env python
# Created by BBruceyuan on 18-7-12.

from .. import db
from . import api
from ..model import Post
from flask import current_app, request, url_for, jsonify, g
from .errors import forbidden
from .authentication import auth
from ..model import CategoryUtil, TagUtil


# 这个posts后面加不加 / 影响前端代码
@api.route('/posts', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,
        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page - 1)
    next_ = None
    if pagination.has_next:
        next_ = url_for('api.get_posts', page=page + 1)
    return jsonify(
        {
            'posts': [post.to_json() for post in posts],
            'prev': prev,
            'next': next_,
            'count': pagination.total})


@api.route('/posts', methods=['POST'])
@auth.login_required
def new_post():
    print('number one test')
    post_json = request.get_json()
    print('test')
    print(post_json)
    post = Post.from_json(post_json)
    post.author = g.current_user
    tags = post_json.get('tags')
    for tag in TagUtil().add_tags(tags):
        post.tags.append(tag)
    categories = post_json.get('categories')
    for category in CategoryUtil().add_categories(categories):
        post.categories.append(category)
    db.session.add(post)
    db.session.commit()
    # 返回值是一个response, 是一个三元组
    # (response, status_code, headers)
    # 关于　后面的 headers，　这是一个字典。
    # 其中 {'location': url_for},　这其实是一个重定向
    # todo, this should think twice
    return jsonify(post.to_json()), 201


@api.route('/posts/<int:pid>')
def get_post(pid):
    post = Post.query.get_or_404(pid)
    return jsonify(post.to_json())


@api.route('/posts/<int:pid>', methods=['PUT'])
@auth.login_required
def update_post(pid):
    post = Post.query.get_or_404(pid)
    if g.current_user != post.author:
        return forbidden('Insufficient permissions, it\'s not your post')
    post.body = request.json.get('body', post.body)
    post.title = request.json.get('title', post.title)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())


@api.route('/posts/<int:pid>', methods=['DELETE'])
@auth.login_required
def delete_post(pid):
    post = Post.query.get_or_404(pid)
    title = post.title
    db.session.delete(post)
    db.session.commit()
    response_json = {
        'title': title,
        'type': 'delete',
        'error_code': 0
    }
    return jsonify(response_json)


