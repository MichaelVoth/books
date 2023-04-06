from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.authors = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def book_select_all(cls):
        query = """SELECT * FROM books;"""
        results = connectToMySQL("books_schema").query_db(query)
        books = []
        for book_dict in results:
            books.append(cls(book_dict))
        return books
    
    @classmethod
    def book_create(cls, data):     #Adds form data to DB as new row
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        results = connectToMySQL("books_schema").query_db(query,data)
        return results
    
    @classmethod
    def get_authors_who_favorited_book(book_id):
        query = """SELECT * 
                    FROM authors
                    LEFT JOIN favorites ON authors.id = favorites.author_id
                    WHERE favorites.book_id = %(book_id)s"""
        data = {
            "book_id": book_id
        }
        results = connectToMySQL("books_schema").query_db(query, data)
        authors = []
        for author_dict in results:
            authors.append(author.Author(author_dict))
        return authors
    
    @classmethod
    def book_select_unfavorited(cls, author_id):
        query = """
            SELECT DISTINCT book_id, books.title
            FROM books
            LEFT JOIN favorites ON favorites.book_id = books.id
            WHERE favorites.author_id IS NULL OR favorites.author_id != %(author_id)s;
        """
        data = {
            "author_id": author_id
        }
        results = connectToMySQL("books_schema").query_db(query, data)
        books = []
        for book_dict in results:
            books.append(cls(book_dict))
        return books
    
    @classmethod
    def book_delete(cls, id):        #Deletes one row from DB
        query  = "DELETE FROM books WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL('books_schema').query_db(query, data) 