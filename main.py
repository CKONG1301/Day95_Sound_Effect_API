import requests
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)
URL = 'https://freesound.org/apiv2/search/text'


class SearchForm(FlaskForm):
    text = StringField("Enter Sound Type", validators=[DataRequired()])
    submit = SubmitField("Search")


@app.route('/', methods=['GET', 'POST'])
def home():
    response = []
    form = SearchForm()
    if form.validate_on_submit():
        query = {
            'query': form.text.data.lower(),
            'fields': "id,url,name,license,username,images,similar_sounds",
            'token': os.getenv('API_KEY'),
        }
        response = requests.get(url=URL, params=query).json()['results']
    return render_template("index.html", form=form, data=response)


if __name__ == "__main__":
    app.run(debug=True)