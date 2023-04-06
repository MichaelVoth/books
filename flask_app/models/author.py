from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book


class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.books = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def author_select_all(cls):
        query = """
                SELECT * FROM authors;"""
        results = connectToMySQL("books_schema").query_db(query)
        authors = []
        for author_dict in results:
            authors.append(cls(author_dict))
        return authors
    
    @classmethod
    def author_create(cls, data):     #Adds form data to DB as new row
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        results = connectToMySQL("books_schema").query_db(query,data)
        return results

    @classmethod
    def get_books_favorited_by_author(cls,id):
        query = """SELECT * FROM authors
                    LEFT JOIN favorites ON favorites.author_id = authors.id
                    LEFT JOIN books ON books.id = favorites.book_id
                    WHERE favorites.author_id = %(author_id)s"""
        data = {
            "author_id": id
        }
        results = connectToMySQL("books_schema").query_db(query, data)
        author = cls( results[0] )
        for row_from_db in results:
            book_data = {
                "id" : row_from_db["id"],
                "title" : row_from_db["title"],
                "num_of_pages" : row_from_db["num_of_pages"],
                "created_at" : row_from_db["books.created_at"],
                "updated_at" : row_from_db["books.updated_at"]
            }
            author.books.append( book.Book( book_data ) )
        return author

    @classmethod
    def author_select_unfavorited(cls, book_id):
        query = """
            SELECT *
            FROM authors
            LEFT JOIN favorites ON favorites.author_id = authors.id
            WHERE favorites.book_id IS NULL OR favorites.book_id != %(book_id)s;
        """
        data = {
            "boook_id": book_id
        }
        results = connectToMySQL("books_schema").query_db(query, data)
        authors = []
        for author_dict in results:
            authors.append(cls(author_dict))
        return authors

    @classmethod
    def author_delete(cls, id):        #Deletes one row from DB
        query  = "DELETE FROM authors WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL('books_schema').query_db(query, data)
    
