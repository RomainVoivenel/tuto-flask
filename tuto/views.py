from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import *
from flask_wtf import FlaskForm
from flask_login import login_user, current_user, logout_user
from flask import request
from wtforms import StringField , HiddenField
from wtforms.validators import DataRequired
from wtforms import PasswordField
from hashlib import sha256

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])
    
class BookForm(FlaskForm):
    id = HiddenField('id')
    title = StringField('Title', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    img = StringField('Image', validators=[DataRequired()])
    url = StringField('Url', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    
    def get_authenticated_user(self) -> User | None:
        user:User = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

@app.route("/")
def home():
    author_id = request.args.get('input_value')

    if author_id is None or author_id == 'All book':
        books = get_sample()
    else:
        books = get_book_by_author(author_id)

    return render_template(
        "home.html",
        title="My Books",
        books=books,
        authors=search_books_by_author()
    )

@app.route("/detail/<id>")
def detail(id):
    return render_template (
        "detail.html",
        title="My Book",
        book=get_book(id))
    
@app.route("/edit/author/<int:id>")
def edit_author(id):
    books = get_book_by_author(id)
        
    a:Author = get_author(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template(
        "edit-author.html",
        author=a, form=f, books=books)
    
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
        "edit-author.html",
        author =a, form=f)
    
@app.route("/edit/book/<int:id>")
def edit_book(id):
    b:Book = get_book(id)
    f = BookForm(id=b.id, title=b.title, price=b.price)
    return render_template(
        "edit-book.html",
        book=b, form=f)
    
@app.route("/add/book/")
def add_book(id):
    b = Book(
    price=19.99,
    title="Le titre du livre",
    url="http://example.com",
    img="http://example.com/image.jpg",
    author_id=1
    )
    f = BookForm(id=b.id, title=b.title, price=b.price, img=b.img, url=b.url, author=b.author)
    return render_template(
        "edit-book.html",
        book=b, form=f)

@app.route("/save/book/", methods=("POST",))
def save_book():
    b = None
    f:BookForm = BookForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        b:Book = get_book(id)
        b.title = f.title.data
        b.price = f.price.data
        db.session.commit()
        return redirect(url_for('edit_book', id=b.id))
    b = get_book(int(f.id.data))
    return render_template (
        "edit-book.html",
        book =b, form=f)

@app.route("/auteur")
def auteur():
    return render_template (
        "auteur.html",
        title="The author",
        authors = get_sample_authors())


@app.route('/search')
def search():
    # Récupère la valeur de l'input "input_value" depuis le formulaire
    search_val = request.args.get('input_value')  
    books = []
    
    if search_val is not None:
        books = search_books_by_author_or_title(search_val)
    
    return render_template('search.html', title='Résultats de recherche', books=books)



    
@app.route("/login/", methods=("GET","POST",))
def login():
    f:LoginForm = LoginForm()
    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            print(user.username + " " + user.password)
            login_user(user)
            return redirect(url_for("home"))
    return render_template(
        "login.html",
        form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))

