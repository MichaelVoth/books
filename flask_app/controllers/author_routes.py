from flask import render_template, redirect, request    #Imports flask functionalilty
from flask_app import app   #Imports flask app
from flask_app.models.author import Author #imports Author class
from flask_app.models.book import Book

@app.route('/')             #quick redirect
def index_redirect():
    return redirect('/authors')

@app.route('/authors')
def show_all_authors():
    all_authors = Author.author_select_all()
    return render_template('authors.html', authors=all_authors)

@app.route('/create_author', methods=['POST'])
def create_author():          #creates an author
    Author.author_create(request.form)
    return redirect('/authors')

@app.route('/authors/<int:id>')
def show_author(id):          #shows author with favorited books
    author = Author.get_books_favorited_by_author(id)
    # nonfavorite_books = Book.book_select_all()
    return render_template('author_show.html', author=author)

@app.route('/delete/<int:id>')
def delete_author(id):        #deletes an author
    Author.author_delete(id)
    return redirect('/authors')