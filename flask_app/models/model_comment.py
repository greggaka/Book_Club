from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import DATABASE, app
from flask_app.models import model_user
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.user_id = data['user_id']
        self.book_id = data['book_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    #Create
    @classmethod
    def add (cls, data):
        query = "INSERT INTO comments (comment) VALUES (%(comment)s);"
        comment_id = MySQLConnection(DATABASE).query_db(query, data)
        return comment_id
    
    #Read All
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM comments LEFT JOIN users on comments.user_id = users.id;"
        results = connectToMySQL(DATABASE). query_db(query)
        if not results:
            return[]
        
        all_comments = []
        for dict in results:
            comment = cls(dict)
            user = {
                **dict,
                'id':dict['users.id'],
                'created_at': ['users.created_at'],
                'updated_at': ['users.updated_at'],
                'password': None
            }
            comment.user = model_user.User(user)
            all_comments.append(comment)
        return all_comments
    
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