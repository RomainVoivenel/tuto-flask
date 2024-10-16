from .app import db
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
    
    def get_is(self):
        return self.username
    
def get_sample():
    return Book.query.limit(18).all()
    
def get_book(id):
    return Book.query.get_or_404(id)

def get_author(id):
    return Author.query.get_or_404(id)

def search_books_by_author(author_name):
    print(author_name)
    return Book.query.join(Author).filter(Author.name.like(f'%{author_name}%')).limit(18).all()

