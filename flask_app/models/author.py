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
    def author_select_one(cls, id):
        query = "SELECT * FROM authors WHERE id=%(id)s"
        results = connectToMySQL('books_schema').query_db(query, {'id': id})
        author = cls(results[0])
        return author 

    @classmethod
    def author_create(cls, data):  # Adds form data to DB as new row
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        results = connectToMySQL("books_schema").query_db(query, data)
        return results

    @classmethod
    def get_books_favorited_by_author(cls, id):
        query = """SELECT * FROM authors
                    LEFT JOIN favorites ON favorites.author_id = authors.id
                    LEFT JOIN books ON books.id = favorites.book_id
                    WHERE favorites.author_id = %(author_id)s"""
        data = {
            "author_id": id
        }
        results = connectToMySQL("books_schema").query_db(query, data)
        if len(results)>0:
            author = cls(results[0])
            for row_from_db in results:
                    book_data = {
                        "id": row_from_db["books.id"],
                        "title": row_from_db["title"],
                        "num_of_pages": row_from_db["num_of_pages"],
                        "created_at": row_from_db["books.created_at"],
                        "updated_at": row_from_db["books.updated_at"]
                    }
                    author.books.append(book.Book(book_data))
            return author
        else:
            author = Author.author_select_one(id)
            return author

    # @classmethod
    # def author_select_unfavorited(cls, author_id): #REWORK TO A NESTED QUERY. SELECT NOT IN (Favorites query)
    #     query = """
    #         SELECT * FROM books WHERE id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(author_id)s);
    #     """
    #     data = {
    #         "author_id": author_id
    #     }
    #     results = connectToMySQL("books_schema").query_db(query, data)
    #     books = []
    #     for book_dict in results:
    #         books.append(cls(book_dict))
    #     return books

    @classmethod
    def author_delete(cls, id):  # Deletes one row from DB
        query = "DELETE FROM authors WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def add_favorite(cls, data):  # query to add book to favorite list
        query = """INSERT INTO favorites (author_id, book_id)
                VALUES (%(author_id)s, %(book_id)s)"""
        return connectToMySQL('books_schema').query_db(query, data)
