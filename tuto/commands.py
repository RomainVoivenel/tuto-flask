import click
from .app import app, db

@app.cli.command()
@click.argument("filename")
def loaddb(filename):
    '''Creates the tables and populates them with data'''
    
    #Création de toute les tables
    db.create_all()
    
    #chargement de notre jeu de données
    import yaml
    books = yaml.safe_load(open(filename))
    
    # imports des models
    from .models import Author, Book
    
    #premiere pass: création de tous les autheurs
    authors = {}
    for b in books:
        autheur_livre = b["author"]
        if autheur_livre not in authors:
            autheur = Author(name=autheur_livre)
            db.session.add(autheur)
            authors[autheur_livre] = autheur
    db.session.commit()
    
    #deuxieme passe: création de tous les livres
    for book in books:
        a = authors[book["author"]]
        o = Book(price = book["price"],
                 title = book["title"],
                 url = book["url"],
                 img = book["img"],
                 author_id = a.id)
        db.session.add(o)
    db.session.commit()
    
@app.cli.command()
def syncdb():
    '''Create all missing tables'''
    db.create_all()