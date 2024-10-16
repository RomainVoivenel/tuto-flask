from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import *
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms . validators import DataRequired

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])

@app.route("/")
def home():
    print(get_sample())
    return render_template (
        "home.html",
        title="My Books",
        books =get_sample())

@app.route("/detail/<id>")
def detail(id):
    return render_template (
        "detail.html",
        title="My Book",
        book=get_book(id))
    
@app.route("/edit/author/<int:id>")
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template(
        "edit-author.html",
        author=a, form=f)
    
@app.route("/save/author/", methods=("POST",))
def save_author():
    a = None
    f = AuthorForm ()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_author(id)
        a.name = f.name.data
        db. session.commit()
        return redirect(url_for('edit_author', id=a.id))
    a = get_author(int(f.id.data))
    return render_template (
        "edit - author.html",
        author =a, form=f)

@app.route('/search')
def search():
    # Récupère la valeur de l'input "input_value" depuis le formulaire
    search_val = request.args.get('input_value')  
    books = []
    
    if search_val is not None:
        books = search_books_by_author_or_title(search_val)
    
    return render_template('search.html', title='Résultats de recherche', books=books)


