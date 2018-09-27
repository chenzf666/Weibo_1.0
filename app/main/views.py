# -*- coding: utf-8 -*-
import datetime
import os
import urllib

from flask import abort, request, current_app, make_response, jsonify
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from .. import db
from ..decorators import admin_required, permission_required
from ..models.comment_model import Comment
from ..models.image_model import Image
from ..models.permission_model import Permission
from ..models.post_model import Post
from ..models.role_model import Role
from ..models.user_model import User
from ..models.video_model import Video

print(Video.__tablename__)


@main.route('/hello')
def hello():
    return render_template('hello.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.name.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('已更新你的资料')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('已更新你的资料')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        if request.form.get('imgArray') is not None:
            images = request.form.get('imgArray').split()
            for img in images:
                img = Image(username=current_user.username, filename=img, post=post)
                db.session.add(img)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))

    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config[
        'FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination, show_followed=show_followed)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user.id != post.author_id and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if request.form.get('imgArray') is not None:
            img_name_init = [pic.filename for pic in post.images.all()]
            img_name = request.form.get('imgArray').split()
            img_name_remove = list(set(img_name_init).difference(set(img_name)))
            img_name_add = list(set(img_name).difference(set(img_name_init)))
            for filename in img_name_remove:
                img = Image.query.filter_by(filename=filename).first()
                db.session.delete(img)
            for filename in img_name_add:
                img = Image(username=post.author.username, filename=filename, post=post)
                db.session.add(img)
        post.body = form.body.data
        db.session.add(post)
        flash('更新成功')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form, post=post)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效用户')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('你已关注该up主')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('成功关注该up主({})'.format(username))
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效用户')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('你没有关注该up主')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('成功取消关注该up主({})'.format(username))
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
                                         error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, pagination=pagination, follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'], error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followed_by.html', user=user, pagination=pagination, follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        flash('评论成功')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = int((post.comments.count() - 1) / current_app.config['FLASKY_COMMENTS_PER_PAGE']) + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=current_app.config[
        'FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form, comments=comments, pagination=pagination)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page=current_app.config[
        'FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments, pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))


@main.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('image')
    folder = current_app.config['STATIC_PATH'] + '/static/uploads/' + str(current_user.username)
    if not os.path.exists(folder):
        os.makedirs(folder)
    img_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_') + secure_filename(file.filename)
    file_path = folder + '/' + img_name
    file.save(file_path)
    URL = urllib.parse.quote(file_path[file_path.index('/static'):])
    # 绝对路径
    return jsonify({'imgURL': URL, 'filename': img_name})


@main.route('/upload/cancel', methods=['POST'])
@login_required
def upload_cancel():
    path = urllib.parse.unquote(request.form.get('src'))
    os.remove('app' + path)
    return make_response('The uploaded image has been deleted.')


@main.route('/upload/delete', methods=['POST'])
@login_required
def upload_delete():
    post_id = request.form.get('post_id')
    images = request.form.get('imgArray').split()
    if post_id is None:
        images_remove = images
        username = current_user.username
    else:
        post = Post.query.filter_by(id=post_id).first()
        username = post.author.username
        images_init = post.images
        images_remove = list(set(images).difference(set(images_init)))
    for filename in images_remove:
        os.remove('{}/static/uploads/{}/{}'.format(current_app.config['STATIC_PATH'], username, filename))
    return make_response('The uploaded image has been deleted.')
