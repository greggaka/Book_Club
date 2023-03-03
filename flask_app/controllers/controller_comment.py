from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User
from flask_app.models.model_book import Book
from flask_app.models.model_comment import Comment
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Post request to save new comment form to data base
@app.route('/comment', methods=["POST"])
def add_comment():
    data={
        **request.form,
        'user_id': session['id']
    }
    Comment.add(data)
    return redirect('/books/<int:id>')