from .app import app
from flask import render_template
import yaml, os.path

data = yaml.safe_load(
                open(
                    os.path.join(
                        os.path. dirname ( __file__ ),
                        "data.yml")))

@app.route("/")
def home ():
    return render_template (
        "home.html",
        title="Hello World!",
        names =["Pierre", "Paul", " Corinne "])