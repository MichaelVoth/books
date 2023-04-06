from flask import render_template, redirect, request    #Imports flask functionalilty
from flask_app import app   #Imports flask app
from flask_app.models.book import Book #imports Book class

@app.route('/books')
def show_all_books():
    all_books = Book.book_select_all()
    return render_template('books.html', books=all_books)

@app.route('/create_book', methods=['POST'])
def create_book():          #creates an book
    Book.book_create(request.form)
    return redirect('/books')

@app.route('/books/<int:id>')
def show_book(id):          #shows author with favorited books
    book = Book.get_authors_who_favorited_book({'id': id})
    return render_template('book_show.html', book=book)

@app.route('/delete/<int:id>')
def delete_book(id):        #deletes an author
    Book.book_delete(id)
    return redirect('/books')