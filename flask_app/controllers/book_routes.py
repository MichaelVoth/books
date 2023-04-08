from flask import render_template, redirect, request    #Imports flask functionalilty
from flask_app import app   #Imports flask app
from flask_app.models.book import Book #imports Book class
from flask_app.models.author import Author

@app.route('/books')
def show_all_books():
    all_books = Book.book_select_all()
    return render_template('books.html', books=all_books)

@app.route('/create_book', methods=['POST'])
def create_book():          #creates an book
    Book.book_create(request.form)
    return redirect('/books')

@app.route('/books/<int:id>')
def show_book(id):          #shows book with favorited authors
    book = Book.get_authors_who_favorited_book(id)
    authors = Author.author_select_all()
    favorite_authors = []
    non_favorite_authors = []
    for author in book.authors:
        favorite_authors.append(author.id)
    for author in authors:
        if author.id not in favorite_authors:
            non_favorite_authors.append(author)
    return render_template('book_show.html', author=non_favorite_authors, book=book)

@app.route("/add_favorite_author", methods=['POST'])
def add_author_to_favorites():
    Author.add_favorite(request.form)
    return redirect(f"/books/{request.form['book_id']}")

@app.route('/delete/<int:id>')
def delete_book(id):        #deletes an author
    Book.book_delete(id)
    return redirect('/books')