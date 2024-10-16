from .app import db, login_manager
from flask_login import UserMixin

class Author (db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String (100))
    
    def __repr__(self):
        return f"<Author ({self.id}) {self.name}>"
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    price = db.Column(db.Float)
    title = db.Column(db.String(150))
    url = db.Column(db.String(150))
    img = db.Column(db.String(150))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref=db.backref("book", lazy="dynamic"))
    
    def __repr__(self):
        return f"<Book {self.id, self.title}>"
    
class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(255))
    
    def get_id(self):
        return self.username
    
def get_sample():
    return Book.query.limit(18).all()
    
def get_book(id):
    return Book.query.get_or_404(id)

def get_author(id):
    return Author.query.get_or_404(id)


from sqlalchemy import or_

def search_books_by_author_or_title(search_val):
    return Book.query.join(Author).filter(or_( #Permet d'imposer de recherche un 'or'
            Author.name.like(f'%{search_val}%'),  # Rechercher parmi les auteurs si le search_val y est
            Book.title.like(f'%{search_val}%')    # Rechercher parmi les titres de livre si le search_val y est
            )).limit(18).all()



@login_manager.user_loader
def load_user(username):
    return User.query.get_or_404(username)

