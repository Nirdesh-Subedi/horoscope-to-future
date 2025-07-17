from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Post, Comment, Like, Reel, ReelLike, ReelComment, Follow, Message, User
from forms import PostForm, CommentForm, ReelForm, MessageForm
from datetime import datetime
import os
from app import app
from werkzeug.utils import secure_filename

social = Blueprint('social', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@social.route('/feed')
@login_required
def feed():
    # Get posts from users that current_user follows
    following_ids = [f.followed_id for f in current_user.following]
    following_ids.append(current_user.id)  # Include own posts
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.user_id.in_(following_ids)) \
        .order_by(Post.created_at.desc()) \
        .paginate(page=page, per_page=10)
    
    form = PostForm()
    return render_template('social/feed.html', posts=posts, form=form)

@social.route('/post/new', methods=['POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            image_file = form.image.data
            if allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'posts', filename)
                image_file.save(image_path)
                image_file = f'uploads/posts/{filename}'
        
        post = Post(
            content=form.content.data,
            image=image_file,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
    return redirect(url_for('social.feed'))

@social.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            post_id=post_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    return redirect(url_for('social.feed'))

@social.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'liked': False, 'count': len(post.likes)})
    else:
        like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'liked': True, 'count': len(post.likes)})

@social.route('/reels')
@login_required
def reels():
    page = request.args.get('page', 1, type=int)
    reels = Reel.query \
        .order_by(Reel.created_at.desc()) \
        .paginate(page=page, per_page=app.config['REELS_PER_PAGE'])
    
    form = ReelForm()
    return render_template('social/reels.html', reels=reels, form=form)

@social.route('/reel/new', methods=['POST'])
@login_required
def new_reel():
    form = ReelForm()
    if form.validate_on_submit():
        if form.video.data and allowed_file(form.video.data.filename):
            video_file = form.video.data
            filename = secure_filename(video_file.filename)
            video_path = os.path.join(app.config['REELS_FOLDER'], filename)
            video_file.save(video_path)
            
            reel = Reel(
                video=f'uploads/reels/{filename}',
                caption=form.caption.data,
                user_id=current_user.id
            )
            db.session.add(reel)
            db.session.commit()
            flash('Your reel has been posted!', 'success')
        else:
            flash('Invalid file format', 'danger')
    return redirect(url_for('social.reels'))

@social.route('/reel/<int:reel_id>/like', methods=['POST'])
@login_required
def like_reel(reel_id):
    reel = Reel.query.get_or_404(reel_id)
    like = ReelLike.query.filter_by(user_id=current_user.id, reel_id=reel.id).first()
    
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'liked': False, 'count': len(reel.reel_likes)})
    else:
        like = ReelLike(user_id=current_user.id, reel_id=reel.id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'liked': True, 'count': len(reel.reel_likes)})

@social.route('/reel/<int:reel_id>/comment', methods=['POST'])
@login_required
def comment_reel(reel_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = ReelComment(
            content=form.content.data,
            user_id=current_user.id,
            reel_id=reel_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    return redirect(url_for('social.reels'))

@social.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        users = User.query.filter(
            (User.username.ilike(f'%{query}%')) | 
            (User.email.ilike(f'%{query}%'))
        ).paginate(page=page, per_page=10)
    else:
        users = User.query.paginate(page=page, per_page=10)
    
    return render_template('social/search.html', users=users, query=query)

@social.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    user = User.query.get_or_404(user_id)
    
    if user == current_user:
        flash('You cannot follow yourself!', 'warning')
        return redirect(url_for('social.search'))
    
    if current_user.is_following(user):
        current_user.unfollow(user)
        return jsonify({'followed': False, 'count': len(user.followers)})
    else:
        current_user.follow(user)
        return jsonify({'followed': True, 'count': len(user.followers)})

@social.route('/messages')
@login_required
def messages():
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) | 
        (Message.recipient_id == current_user.id)
    ).order_by(Message.created_at.desc()).all()
    
    # Get unique conversations
    conversations = {}
    for msg in messages:
        other_id = msg.sender_id if msg.sender_id != current_user.id else msg.recipient_id
        if other_id not in conversations:
            other_user = User.query.get(other_id)
            conversations[other_id] = {
                'user': other_user,
                'last_message': msg,
                'unread': False
            }
        if msg.recipient_id == current_user.id and not msg.is_read:
            conversations[other_id]['unread'] = True
    
    return render_template('social/messages.html', conversations=conversations.values())

@social.route('/messages/<int:user_id>', methods=['GET', 'POST'])
@login_required
def conversation(user_id):
    other_user = User.query.get_or_404(user_id)
    
    # Mark messages as read
    Message.query.filter_by(sender_id=user_id, recipient_id=current_user.id, is_read=False) \
        .update({'is_read': True})
    db.session.commit()
    
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            content=form.content.data,
            sender_id=current_user.id,
            recipient_id=user_id
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('social.conversation', user_id=user_id))
    
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()
    
    return render_template('social/conversation.html', 
                         other_user=other_user, 
                         messages=messages, 
                         form=form)

@social.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).limit(10).all()
    
    is_following = current_user.is_following(user)
    return render_template('social/profile.html', 
                         user=user, 
                         posts=posts, 
                         is_following=is_following)