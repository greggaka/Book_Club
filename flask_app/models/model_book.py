from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import DATABASE, app
from flask_app.models import model_user
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.reader_review = data['reader_review']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comments = []

    #Create
    @classmethod
    def add (cls, data):
        query = "INSERT INTO books (title, author, reader_review, user_id) VALUES (%(title)s, %(author)s, %(reader_review)s, %(user_id)s);"
        user_id = MySQLConnection(DATABASE).query_db(query, data)
        return user_id
    
    #Read All
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books LEFT JOIN users on books.user_id = users.id;"
        results = connectToMySQL(DATABASE). query_db(query)
        if not results:
            return[]
        
        all_books = []
        for dict in results:
            book = cls(dict)
            user = {
                **dict,
                'id':dict['users.id'],
                'created_at': ['users.created_at'],
                'updated_at': ['users.updated_at'],
                'password': None
            }
            book.user = model_user.User(user)
            all_books.append(book)
        return all_books
    
    #Read All for User
    @classmethod
    def get_all_user(cls, data):
        query = 'SELECT * FROM books JOIN users On users.id = books.user_id WHERE users.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return []
        all_user_books = []
        for dict in results:
            book = cls(dict)
            user = {
                **dict,
                'id':dict['users.id'],
                'created_at': ['users.created_at'],
                'updated_at': ['users.updated_at'],
                'password': None
            }
            book.user = model_user.User(user)
            all_user_books.append(book)
        return all_user_books
    
    #Read One
    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM books JOIN users On users.id = books.user_id WHERE books.id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return []
        print (result)
        book = cls(result[0])
        user = {
            **result[0],
                'id' : result[0]['users.id'],
                'created_at' : result[0]['users.created_at'],
                'updated_at' : result[0]['users.updated_at'],
                'password' : None
        }
        book.user = model_user.User(user)
        print(book)
        return book
    
    #Update One
    @classmethod
    def update(cls, data):
        query = "UPDATE books SET title=%(title)s, author=%(author)s, reader_review=%(reader_review)s WHERE books.id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #Delete One
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM books WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #Form Validator
    @staticmethod
    def book_validator(book):
        is_valid = True
        if len(book['title']) < 2:
            flash("'Title' field required. Must be at least 2 characters")
            is_valid = False
        if len(book['author']) < 2:
            flash("'Author' field required. Must be at least 2 characters")
            is_valid = False
        return is_valid
    