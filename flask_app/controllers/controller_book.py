from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User
from flask_app.models.model_book import Book
from flask_app.models.model_comment import Comment
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#GET request to dashboard
#Display route that shows dashboard/table of objects
@app.route('/books/dashboard')
def dashboard():
    print ('test')
    if 'id' not in session:
        return redirect('/logout')
    books = Book.get_all()
    return render_template('book_dashboard.html', books=books)

@app.route('/user/books')
def user_log():
    data = {
        'id': session['id']
    }
    books = Book.get_all_user(data)
    return render_template('user_books.html', books=books)

#Get request to new book form
@app.route('/books/new')
def new_book():
    return render_template('book_new.html')

#Post request to save new book form to data base
@app.route('/books', methods=["POST"])
def add_book():
    if Book.book_validator(request.form):
        data={
            **request.form,
            'user_id': session['id']
        }
        Book.add(data)
        return redirect ('/books/dashboard')
    return redirect('/books/new')

#GET request to show one db entry
#Display route that shows the information for one databas entry
@app.route('/books/<int:id>')
def show_book(id):
    data = {
        'id': id
    }
    book = Book.get_one(data)
    return render_template('book_show.html', book=book)

#GET request to edit car form
#Display route that displays form to edit a db entry's info
@app.route('/books/edit/<int:id>')
def edit_book(id):
    data = {
        'id': id
    }
    book=Book.get_one(data)
    return render_template('book_edit.html', book=book)

#Post request to edit and update car info
#Action route that edits and update db entry according to edit form
@app.route('/books/edit/<int:id>', methods=['POST'])
def edit(id):
    print(id)
    if Book.book_validator(request.form):
        data = {
            **request.form,
            'id':id
        }
        Book.update(data)
        return redirect('/books/dashboard')
    return redirect(f'/books/edit/{id}')

#Get request to delete specific db entry
#Action route that deletes instance from db
@app.route('/books/delete/<int:id>')
def book_delete(id):
    data = {
        'id': id
    }
    Book.delete(data)
    return redirect('/books/dashboard')

@app.route('/books/search')
def book_search():
    return render_template('book_search.html')

