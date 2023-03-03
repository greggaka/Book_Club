from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app.models import model_book
from flask_app import DATABASE, app
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

# class below takes in data from MySQL table/db
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []
        self.comments = []
        
    #Create---------------------------------------
    @classmethod
    def create (cls, data:dict) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return MySQLConnection(DATABASE).query_db(query, data)
    
    @classmethod
    def hash_pw(cls, data):
        query = "INSERT INTO users (email, password) VALUES(%(email)s, %(password)s) WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #Read------------------------------------------
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;" 
        results = connectToMySQL(DATABASE).query_db(query) #returns list of dictionaries
        print (results)
        if not results:
            return []
        
        all_users = []
        for dict in results:
            all_users.append(cls(dict))
            return all_users #returns a list of all instances
        
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users JOIN books ON books.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return[]
        print (results)
        user = cls(results[0])
        for dict in results:
            book = {
                'id': dict['books.id'],
                'title': dict['title'],
                'author': dict['author'],
                'comment': dict['comment'],
                'created_at': dict['books.created_at'],
                'updated_at': dict['books.updated_at']
            }
            user.books.append(model_book.Book(book))
            print(user)
            return user
    
    #For login
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        return cls(result[0])
    
    #Update-----------------------------------------------------
    @classmethod
    def update_one(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #Delete-----------------------------------------------------
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #Form Validator---------------------------------------------
    @staticmethod
    def validate(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name field required. Must be at least 2 characters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name field required. Must be at least 2 characters")
            is_valid = False
        if len(user['email']) <=0:
            flash("Email field required")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        query = "SELECT * From users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, user)
        if len(results)>= 1:
            flash("Email already taken") 
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if (user['password'] != user['confirm_pw']):
            flash("Passwords do not match. Please confirm your password")
            is_valid = False
        return is_valid